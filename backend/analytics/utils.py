from django.utils import timezone
from .models import ProductInteraction, UserBehaviorSummary


def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_session_key(request):
    """Get or create session key."""
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def track_interaction(request, product, interaction_type, metadata=None):
    """
    Track a product interaction.
    
    Args:
        request: Django request object
        product: Product instance
        interaction_type: One of 'view', 'click', 'add_to_cart', 'remove_from_cart', 'purchase'
        metadata: Optional dict with additional data
    """
    user = request.user if request.user.is_authenticated else None
    session_key = get_session_key(request) if not user else None
    
    # Create interaction record
    interaction = ProductInteraction.objects.create(
        product=product,
        user=user,
        session_key=session_key,
        interaction_type=interaction_type,
        metadata=metadata or {},
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        referrer=request.META.get('HTTP_REFERER')
    )
    
    # Update user behavior summary
    update_user_behavior(user, session_key, product, interaction_type)
    
    return interaction


def update_user_behavior(user, session_key, product, interaction_type):
    """Update user behavior summary for analytics."""
    
    # Get or create behavior summary
    if user:
        summary, created = UserBehaviorSummary.objects.get_or_create(
            user=user,
            product=product,
            defaults={'session_key': None}
        )
    else:
        summary, created = UserBehaviorSummary.objects.get_or_create(
            session_key=session_key,
            product=product,
            user=None
        )
    
    now = timezone.now()
    
    if interaction_type == 'view':
        summary.viewed = True
        summary.view_count += 1
        if not summary.first_view_at:
            summary.first_view_at = now
        summary.last_view_at = now
    
    elif interaction_type == 'click':
        summary.clicked = True
    
    elif interaction_type == 'add_to_cart':
        summary.added_to_cart = True
        summary.cart_add_count += 1
        summary.added_to_cart_at = now
        # Reset removed flag when added again
        summary.removed_from_cart = False
    
    elif interaction_type == 'remove_from_cart':
        summary.removed_from_cart = True
        summary.cart_remove_count += 1
        summary.removed_from_cart_at = now
    
    elif interaction_type == 'purchase':
        summary.purchased = True
        summary.purchase_count += 1
        summary.purchased_at = now
    
    summary.save()
