from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random

from analytics.models import ProductInteraction, DailyProductStats, UserBehaviorSummary
from products.models import Product, Category

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with sample analytics data for dashboard'
    
    def handle(self, *args, **options):
        self.stdout.write('Seeding analytics data...')
        
        products = list(Product.objects.filter(is_active=True))
        
        if not products:
            self.stdout.write(self.style.ERROR('No products found. Please run seed_data first.'))
            return
        
        # Get or create test users
        test_users = self.get_or_create_test_users()
        
        # Generate interactions for the last 30 days
        self.generate_interactions(products, test_users)
        
        # Update daily stats
        self.update_daily_stats(products)
        
        # Update user behavior summaries
        self.update_behavior_summaries(products, test_users)
        
        self.stdout.write(self.style.SUCCESS('Analytics data seeded successfully!'))
    
    def get_or_create_test_users(self):
        users = []
        for i in range(5):
            user, created = User.objects.get_or_create(
                email=f'testuser{i+1}@example.com',
                defaults={
                    'username': f'testuser{i+1}',
                    'first_name': f'Test',
                    'last_name': f'User{i+1}',
                    'is_active': True,
                }
            )
            if created:
                user.set_password('test123')
                user.save()
                self.stdout.write(f'Created test user: {user.email}')
            users.append(user)
        return users
    
    def generate_interactions(self, products, users):
        self.stdout.write('Generating product interactions...')
        
        interaction_types = ['view', 'add_to_cart', 'remove_from_cart', 'purchase']
        
        # Clear existing interactions
        ProductInteraction.objects.all().delete()
        
        interactions_created = 0
        
        for day_offset in range(30, 0, -1):
            date = timezone.now() - timedelta(days=day_offset)
            
            # Generate more interactions on weekends
            is_weekend = date.weekday() >= 5
            base_interactions = random.randint(50, 150) if is_weekend else random.randint(30, 100)
            
            for _ in range(base_interactions):
                product = random.choice(products)
                user = random.choice(users + [None, None, None])  # 60% chance of anonymous
                
                # Views happen most often
                interaction_type = random.choices(
                    interaction_types,
                    weights=[70, 15, 5, 10],
                    k=1
                )[0]
                
                # Add some variation to the time
                hour = random.randint(6, 23)
                minute = random.randint(0, 59)
                interaction_time = date.replace(hour=hour, minute=minute)
                
                metadata = {}
                if interaction_type in ['add_to_cart', 'purchase']:
                    metadata['quantity'] = random.randint(1, 3)
                if interaction_type == 'purchase':
                    metadata['order_id'] = f'ORD-{random.randint(10000, 99999)}'
                
                session_key = None if user else f'session_{random.randint(10000, 99999)}'
                
                ProductInteraction.objects.create(
                    product=product,
                    user=user,
                    session_key=session_key,
                    interaction_type=interaction_type,
                    metadata=metadata,
                    created_at=interaction_time
                )
                interactions_created += 1
        
        self.stdout.write(f'Created {interactions_created} interactions')
    
    def update_daily_stats(self, products):
        self.stdout.write('Updating daily product stats...')
        
        DailyProductStats.objects.all().delete()
        
        for day_offset in range(30, 0, -1):
            date = (timezone.now() - timedelta(days=day_offset)).date()
            
            for product in products:
                interactions = ProductInteraction.objects.filter(
                    product=product,
                    created_at__date=date
                )
                
                views = interactions.filter(interaction_type='view').count()
                add_to_cart = interactions.filter(interaction_type='add_to_cart').count()
                purchases = interactions.filter(interaction_type='purchase').count()
                
                if views > 0 or add_to_cart > 0 or purchases > 0:
                    revenue = sum(
                        float(product.final_price) * i.metadata.get('quantity', 1)
                        for i in interactions.filter(interaction_type='purchase')
                    )
                    
                    DailyProductStats.objects.create(
                        product=product,
                        date=date,
                        view_count=views,
                        cart_add_count=add_to_cart,
                        purchase_count=purchases,
                        revenue=revenue
                    )
        
        self.stdout.write('Daily stats updated')
    
    def update_behavior_summaries(self, products, users):
        self.stdout.write('Updating user behavior summaries...')
        
        UserBehaviorSummary.objects.all().delete()
        
        for product in products:
            for user in users:
                interactions = ProductInteraction.objects.filter(
                    product=product,
                    user=user
                )
                
                if not interactions.exists():
                    continue
                
                view_count = interactions.filter(interaction_type='view').count()
                cart_add_count = interactions.filter(interaction_type='add_to_cart').count()
                cart_remove_count = interactions.filter(interaction_type='remove_from_cart').count()
                purchase_count = interactions.filter(interaction_type='purchase').count()
                
                if view_count > 0:
                    UserBehaviorSummary.objects.create(
                        product=product,
                        user=user,
                        session_key=None,
                        viewed=view_count > 0,
                        view_count=view_count,
                        added_to_cart=cart_add_count > 0,
                        cart_add_count=cart_add_count,
                        removed_from_cart=cart_remove_count > 0,
                        cart_remove_count=cart_remove_count,
                        purchased=purchase_count > 0,
                        purchase_count=purchase_count
                    )
        
        # Also create some anonymous behavior summaries
        sessions = ProductInteraction.objects.filter(
            session_key__isnull=False
        ).values_list('session_key', flat=True).distinct()[:20]
        
        for session_key in sessions:
            for product in random.sample(list(products), min(5, len(products))):
                interactions = ProductInteraction.objects.filter(
                    product=product,
                    session_key=session_key
                )
                
                view_count = interactions.filter(interaction_type='view').count()
                cart_add_count = interactions.filter(interaction_type='add_to_cart').count()
                cart_remove_count = interactions.filter(interaction_type='remove_from_cart').count()
                purchase_count = interactions.filter(interaction_type='purchase').count()
                
                if view_count > 0:
                    UserBehaviorSummary.objects.create(
                        product=product,
                        user=None,
                        session_key=session_key,
                        viewed=view_count > 0,
                        view_count=view_count,
                        added_to_cart=cart_add_count > 0,
                        cart_add_count=cart_add_count,
                        removed_from_cart=cart_remove_count > 0,
                        cart_remove_count=cart_remove_count,
                        purchased=purchase_count > 0,
                        purchase_count=purchase_count
                    )
        
        self.stdout.write('Behavior summaries updated')
