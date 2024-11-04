from celery import shared_task
from .models import Order
from django.core.cache import cache

@shared_task
def process_order(order_id):
    try:
        order = Order.objects.get(id=order_id)

        cache.set(f'order_{order.id}', order.user, timeout=60*5)

        print(f"Order {order.id} has been successfully processed!")
        
    except Order.DoesNotExist:
        print(f"Order with id {order_id} does not exist.")
    except Exception as e:
        print(f"An error occurred while processing order {order_id}: {str(e)}")
