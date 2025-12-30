from .utils import track_interaction, get_session_key, get_client_ip
from products.models import Product


class InteractionTrackingMiddleware:
    """Middleware to track product views automatically."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Ensure session exists for anonymous users
        if not request.session.session_key:
            request.session.create()
        
        response = self.get_response(request)
        return response
