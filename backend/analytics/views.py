from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Count, F, Q, Avg
from django.db.models.functions import TruncDate, Coalesce
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta
import io
import csv

from .models import ProductInteraction, DailyProductStats, UserBehaviorSummary
from .serializers import (
    ProductInteractionSerializer, TrackInteractionSerializer,
    ProductAnalyticsSummarySerializer, CategoryAnalyticsSummarySerializer,
    TimeSeriesDataSerializer, FunnelDataSerializer
)
from .utils import track_interaction
from products.models import Product, Category


class TrackInteractionView(APIView):
    """Track product interaction from frontend."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = TrackInteractionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product = get_object_or_404(Product, id=serializer.validated_data['product_id'])
        
        track_interaction(
            request=request,
            product=product,
            interaction_type=serializer.validated_data['interaction_type'],
            metadata=serializer.validated_data.get('metadata', {})
        )
        
        return Response({'message': 'Interaction tracked successfully'})


class IsAdminOrStaff(permissions.BasePermission):
    """Permission check for admin/staff users."""
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_staff or request.user.is_superuser
        )


# Admin Analytics Views
class DashboardOverviewView(APIView):
    """Get dashboard overview statistics."""
    
    permission_classes = [IsAdminOrStaff]
    
    def get(self, request):
        # Date range from query params
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        # Get interactions in date range
        interactions = ProductInteraction.objects.filter(created_at__gte=start_date)
        
        # Overview stats
        total_views = interactions.filter(interaction_type='view').count()
        total_add_to_cart = interactions.filter(interaction_type='add_to_cart').count()
        total_purchases = interactions.filter(interaction_type='purchase').count()
        total_remove_from_cart = interactions.filter(interaction_type='remove_from_cart').count()
        
        # Revenue calculation
        purchase_interactions = interactions.filter(interaction_type='purchase')
        total_revenue = 0
        for interaction in purchase_interactions:
            quantity = interaction.metadata.get('quantity', 1)
            total_revenue += float(interaction.product.final_price) * quantity
        
        # Unique users/sessions
        unique_users = interactions.exclude(user__isnull=True).values('user').distinct().count()
        unique_sessions = interactions.exclude(session_key__isnull=True).values('session_key').distinct().count()
        
        # Conversion rates
        view_to_cart_rate = (total_add_to_cart / total_views * 100) if total_views > 0 else 0
        cart_to_purchase_rate = (total_purchases / total_add_to_cart * 100) if total_add_to_cart > 0 else 0
        overall_conversion = (total_purchases / total_views * 100) if total_views > 0 else 0
        
        # Cart abandonment
        cart_abandonment_rate = (total_remove_from_cart / total_add_to_cart * 100) if total_add_to_cart > 0 else 0
        
        return Response({
            'period_days': days,
            'total_views': total_views,
            'total_add_to_cart': total_add_to_cart,
            'total_purchases': total_purchases,
            'total_remove_from_cart': total_remove_from_cart,
            'total_revenue': round(total_revenue, 2),
            'unique_registered_users': unique_users,
            'unique_anonymous_sessions': unique_sessions,
            'conversion_rates': {
                'view_to_cart': round(view_to_cart_rate, 2),
                'cart_to_purchase': round(cart_to_purchase_rate, 2),
                'overall': round(overall_conversion, 2),
            },
            'cart_abandonment_rate': round(cart_abandonment_rate, 2),
        })


class MostViewedProductsView(APIView):
    """Get most viewed products."""
    
    permission_classes = [IsAdminOrStaff]
    
    def get(self, request):
        days = int(request.query_params.get('days', 30))
        limit = int(request.query_params.get('limit', 10))
        category = request.query_params.get('category')
        
        start_date = timezone.now() - timedelta(days=days)
        
        queryset = ProductInteraction.objects.filter(
            interaction_type='view',
            created_at__gte=start_date
        )
        
        if category:
            queryset = queryset.filter(product__category_id=category)
        
        products = queryset.values(
            'product__id',
            'product__name',
            'product__image',
            'product__category__name'
        ).annotate(
            total_views=Count('id')
        ).order_by('-total_views')[:limit]
        
        result = []
        for item in products:
            result.append({
                'product_id': item['product__id'],
                'product_name': item['product__name'],
                'product_image': item['product__image'],
                'category_name': item['product__category__name'],
                'total_views': item['total_views'],
            })
        
        return Response(result)


class MostAddedToCartProductsView(APIView):
    """Get products most frequently added to cart."""
    
    permission_classes = [IsAdminOrStaff]
    
    def get(self, request):
        days = int(request.query_params.get('days', 30))
        limit = int(request.query_params.get('limit', 10))
        category = request.query_params.get('category')
        
        start_date = timezone.now() - timedelta(days=days)
        
        queryset = ProductInteraction.objects.filter(
            interaction_type='add_to_cart',
            created_at__gte=start_date
        )
        
        if category:
            queryset = queryset.filter(product__category_id=category)
        
        products = queryset.values(
            'product__id',
            'product__name',
            'product__image',
            'product__category__name'
        ).annotate(
            total_adds=Count('id')
        ).order_by('-total_adds')[:limit]
        
        result = []
        for item in products:
            result.append({
                'product_id': item['product__id'],
                'product_name': item['product__name'],
                'product_image': item['product__image'],
                'category_name': item['product__category__name'],
                'total_adds': item['total_adds'],
            })
        
        return Response(result)


class MostPurchasedProductsView(APIView):
    """Get most purchased products."""
    
    permission_classes = [IsAdminOrStaff]
    
    def get(self, request):
        days = int(request.query_params.get('days', 30))
        limit = int(request.query_params.get('limit', 10))
        category = request.query_params.get('category')
        
        start_date = timezone.now() - timedelta(days=days)
        
        queryset = ProductInteraction.objects.filter(
            interaction_type='purchase',
            created_at__gte=start_date
        )
        
        if category:
            queryset = queryset.filter(product__category_id=category)
        
        products = queryset.values(
            'product__id',
            'product__name',
            'product__image',
            'product__category__name',
            'product__price'
        ).annotate(
            total_purchases=Count('id')
        ).order_by('-total_purchases')[:limit]
        
        result = []
        for item in products:
            # Calculate revenue
            purchases = ProductInteraction.objects.filter(
                product_id=item['product__id'],
                interaction_type='purchase',
                created_at__gte=start_date
            )
            revenue = sum(
                float(item['product__price']) * p.metadata.get('quantity', 1)
                for p in purchases
            )
            
            result.append({
                'product_id': item['product__id'],
                'product_name': item['product__name'],
                'product_image': item['product__image'],
                'category_name': item['product__category__name'],
                'total_purchases': item['total_purchases'],
                'total_revenue': round(revenue, 2),
            })
        
        return Response(result)


class ViewedButNotPurchasedView(APIView):
    """Get products viewed but not purchased."""
    
    permission_classes = [IsAdminOrStaff]
    
    def get(self, request):
        days = int(request.query_params.get('days', 30))
        limit = int(request.query_params.get('limit', 10))
        
        # Get products with views but no purchases in the period
        products = UserBehaviorSummary.objects.filter(
            viewed=True,
            purchased=False,
            updated_at__gte=timezone.now() - timedelta(days=days)
        ).values(
            'product__id',
            'product__name',
            'product__image',
            'product__category__name'
        ).annotate(
            view_count=Sum('view_count'),
            unique_viewers=Count('id')
        ).order_by('-view_count')[:limit]
        
        result = []
        for item in products:
            result.append({
                'product_id': item['product__id'],
                'product_name': item['product__name'],
                'product_image': item['product__image'],
                'category_name': item['product__category__name'],
                'total_views': item['view_count'],
                'unique_viewers': item['unique_viewers'],
            })
        
        return Response(result)


class AddedToCartButRemovedView(APIView):
    """Get products added to cart but later removed (not purchased)."""
    
    permission_classes = [IsAdminOrStaff]
    
    def get(self, request):
        days = int(request.query_params.get('days', 30))
        limit = int(request.query_params.get('limit', 10))
        
        products = UserBehaviorSummary.objects.filter(
            added_to_cart=True,
            removed_from_cart=True,
            purchased=False,
            updated_at__gte=timezone.now() - timedelta(days=days)
        ).values(
            'product__id',
            'product__name',
            'product__image',
            'product__category__name'
        ).annotate(
            total_removed=Sum('cart_remove_count'),
            unique_removers=Count('id')
        ).order_by('-total_removed')[:limit]
        
        result = []
        for item in products:
            result.append({
                'product_id': item['product__id'],
                'product_name': item['product__name'],
                'product_image': item['product__image'],
                'category_name': item['product__category__name'],
                'total_removed': item['total_removed'],
                'unique_removers': item['unique_removers'],
            })
        
        return Response(result)


class TimeSeriesAnalyticsView(APIView):
    """Get time series data for charts."""
    
    permission_classes = [IsAdminOrStaff]
    
    def get(self, request):
        days = int(request.query_params.get('days', 30))
        category = request.query_params.get('category')
        product_id = request.query_params.get('product')
        
        start_date = timezone.now() - timedelta(days=days)
        
        queryset = ProductInteraction.objects.filter(created_at__gte=start_date)
        
        if category:
            queryset = queryset.filter(product__category_id=category)
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        
        # Group by date
        data = queryset.annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            views=Count('id', filter=Q(interaction_type='view')),
            add_to_cart=Count('id', filter=Q(interaction_type='add_to_cart')),
            purchases=Count('id', filter=Q(interaction_type='purchase')),
        ).order_by('date')
        
        result = []
        for item in data:
            # Calculate revenue for this date
            date_purchases = queryset.filter(
                interaction_type='purchase',
                created_at__date=item['date']
            )
            revenue = sum(
                float(p.product.final_price) * p.metadata.get('quantity', 1)
                for p in date_purchases
            )
            
            result.append({
                'date': item['date'].isoformat(),
                'views': item['views'],
                'add_to_cart': item['add_to_cart'],
                'purchases': item['purchases'],
                'revenue': round(revenue, 2),
            })
        
        return Response(result)


class CategoryAnalyticsView(APIView):
    """Get analytics by category."""
    
    permission_classes = [IsAdminOrStaff]
    
    def get(self, request):
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        categories = Category.objects.filter(is_active=True)
        
        result = []
        for category in categories:
            interactions = ProductInteraction.objects.filter(
                product__category=category,
                created_at__gte=start_date
            )
            
            views = interactions.filter(interaction_type='view').count()
            add_to_cart = interactions.filter(interaction_type='add_to_cart').count()
            purchases = interactions.filter(interaction_type='purchase').count()
            
            # Calculate revenue
            purchase_interactions = interactions.filter(interaction_type='purchase')
            revenue = sum(
                float(p.product.final_price) * p.metadata.get('quantity', 1)
                for p in purchase_interactions
            )
            
            result.append({
                'category_id': str(category.id),
                'category_name': category.name,
                'total_views': views,
                'total_add_to_cart': add_to_cart,
                'total_purchases': purchases,
                'total_revenue': round(revenue, 2),
                'product_count': category.products.filter(is_active=True).count(),
            })
        
        return Response(sorted(result, key=lambda x: x['total_views'], reverse=True))


class FunnelAnalyticsView(APIView):
    """Get funnel analysis data."""
    
    permission_classes = [IsAdminOrStaff]
    
    def get(self, request):
        days = int(request.query_params.get('days', 30))
        
        # Get total unique visitors (users + sessions)
        start_date = timezone.now() - timedelta(days=days)
        interactions = ProductInteraction.objects.filter(created_at__gte=start_date)
        
        # Count unique visitors who performed each action
        total_visitors = interactions.values('user', 'session_key').distinct().count()
        
        viewed = UserBehaviorSummary.objects.filter(
            viewed=True,
            updated_at__gte=start_date
        ).count()
        
        added_to_cart = UserBehaviorSummary.objects.filter(
            added_to_cart=True,
            updated_at__gte=start_date
        ).count()
        
        purchased = UserBehaviorSummary.objects.filter(
            purchased=True,
            updated_at__gte=start_date
        ).count()
        
        base = viewed if viewed > 0 else 1
        
        funnel = [
            {
                'stage': 'Product Views',
                'count': viewed,
                'percentage': 100.0,
            },
            {
                'stage': 'Added to Cart',
                'count': added_to_cart,
                'percentage': round(added_to_cart / base * 100, 2),
            },
            {
                'stage': 'Completed Purchase',
                'count': purchased,
                'percentage': round(purchased / base * 100, 2),
            },
        ]
        
        return Response(funnel)


class InteractionHistoryView(generics.ListAPIView):
    """Get complete interaction history."""
    
    serializer_class = ProductInteractionSerializer
    permission_classes = [IsAdminOrStaff]
    filterset_fields = ['interaction_type', 'product']
    search_fields = ['product__name', 'user__email']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = ProductInteraction.objects.select_related('product', 'user')
        
        # Filter by date range
        days = self.request.query_params.get('days')
        if days:
            start_date = timezone.now() - timedelta(days=int(days))
            queryset = queryset.filter(created_at__gte=start_date)
        
        # Filter by category
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(product__category_id=category)
        
        return queryset


class ExportAnalyticsView(APIView):
    """Export analytics data as CSV."""
    
    permission_classes = [IsAdminOrStaff]
    
    def get(self, request):
        report_type = request.query_params.get('type', 'interactions')
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{report_type}_report.csv"'
        
        writer = csv.writer(response)
        
        if report_type == 'interactions':
            writer.writerow([
                'Date', 'Product', 'Category', 'Interaction Type',
                'User Email', 'Session Key', 'IP Address'
            ])
            
            interactions = ProductInteraction.objects.filter(
                created_at__gte=start_date
            ).select_related('product', 'product__category', 'user')
            
            for i in interactions:
                writer.writerow([
                    i.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    i.product.name,
                    i.product.category.name,
                    i.interaction_type,
                    i.user.email if i.user else 'Anonymous',
                    i.session_key or '',
                    i.ip_address or '',
                ])
        
        elif report_type == 'products':
            writer.writerow([
                'Product', 'Category', 'Views', 'Add to Cart',
                'Remove from Cart', 'Purchases', 'Revenue'
            ])
            
            products = Product.objects.filter(is_active=True).select_related('category')
            
            for product in products:
                interactions = ProductInteraction.objects.filter(
                    product=product,
                    created_at__gte=start_date
                )
                
                views = interactions.filter(interaction_type='view').count()
                add_to_cart = interactions.filter(interaction_type='add_to_cart').count()
                remove_from_cart = interactions.filter(interaction_type='remove_from_cart').count()
                purchases = interactions.filter(interaction_type='purchase').count()
                
                purchase_interactions = interactions.filter(interaction_type='purchase')
                revenue = sum(
                    float(product.final_price) * p.metadata.get('quantity', 1)
                    for p in purchase_interactions
                )
                
                writer.writerow([
                    product.name,
                    product.category.name,
                    views,
                    add_to_cart,
                    remove_from_cart,
                    purchases,
                    round(revenue, 2),
                ])
        
        elif report_type == 'categories':
            writer.writerow([
                'Category', 'Products', 'Views', 'Add to Cart', 'Purchases', 'Revenue'
            ])
            
            categories = Category.objects.filter(is_active=True)
            
            for category in categories:
                interactions = ProductInteraction.objects.filter(
                    product__category=category,
                    created_at__gte=start_date
                )
                
                views = interactions.filter(interaction_type='view').count()
                add_to_cart = interactions.filter(interaction_type='add_to_cart').count()
                purchases = interactions.filter(interaction_type='purchase').count()
                
                purchase_interactions = interactions.filter(interaction_type='purchase')
                revenue = sum(
                    float(p.product.final_price) * p.metadata.get('quantity', 1)
                    for p in purchase_interactions
                )
                
                writer.writerow([
                    category.name,
                    category.products.filter(is_active=True).count(),
                    views,
                    add_to_cart,
                    purchases,
                    round(revenue, 2),
                ])
        
        return response


class ExportPDFView(APIView):
    """Export analytics data as PDF."""
    
    permission_classes = [IsAdminOrStaff]
    
    def get(self, request):
        from django.http import HttpResponse
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        # Create response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="analytics_report.pdf"'
        
        # Create PDF
        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        elements.append(Paragraph(f"Analytics Report - Last {days} Days", styles['Title']))
        elements.append(Spacer(1, 20))
        
        # Overview stats
        interactions = ProductInteraction.objects.filter(created_at__gte=start_date)
        total_views = interactions.filter(interaction_type='view').count()
        total_cart = interactions.filter(interaction_type='add_to_cart').count()
        total_purchases = interactions.filter(interaction_type='purchase').count()
        
        overview_data = [
            ['Metric', 'Value'],
            ['Total Views', str(total_views)],
            ['Total Add to Cart', str(total_cart)],
            ['Total Purchases', str(total_purchases)],
        ]
        
        overview_table = Table(overview_data, colWidths=[200, 100])
        overview_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(Paragraph("Overview", styles['Heading2']))
        elements.append(overview_table)
        elements.append(Spacer(1, 20))
        
        # Top Products
        elements.append(Paragraph("Top Products by Views", styles['Heading2']))
        
        products = interactions.filter(interaction_type='view').values(
            'product__name'
        ).annotate(
            views=Count('id')
        ).order_by('-views')[:10]
        
        product_data = [['Product', 'Views']]
        for p in products:
            product_data.append([p['product__name'], str(p['views'])])
        
        if len(product_data) > 1:
            product_table = Table(product_data, colWidths=[300, 100])
            product_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(product_table)
        
        doc.build(elements)
        return response
