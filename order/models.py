from django.db import models
from cart.models import Cart
from customer.models import Customer,Address
from product.models import Product

# Create your models here.
class Order(models.Model):
    pending = 'P'
    confirmed = 'C' 
    declined = 'D'
    PAYMENT_STATUS = [(pending, 'Pending'),
                      (confirmed, 'Confirmed'),
                      (declined, 'Declined')]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,
                                 related_name='orders')
    placed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    status = models.CharField(max_length=1, choices=PAYMENT_STATUS,
                              default=pending)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT,
                              related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                related_name='order_items') 
    quantity = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    