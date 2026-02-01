from django.http import JsonResponse
from .models import Order

def get_latest_order_id(request):
    """
    Returns the ID of the most recent order.
    Used by the admin dashboard for sound notifications.
    """
    latest_order = Order.objects.filter(status='CONFIRMED').only('order_id', 'created_at').order_by('-created_at').first()
    return JsonResponse({
        'latest_id': str(latest_order.order_id) if latest_order else None,
        'created_at': latest_order.created_at.timestamp() if latest_order else 0
    })
