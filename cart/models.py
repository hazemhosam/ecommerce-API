from uuid import uuid4
from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
from uuid import uuid4
from django.db import models
from product.models import Product

# Create your models here.
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True) 



class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,
                             related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='cart_items') 
    quantity = models.PositiveBigIntegerField(
        validators=[MinValueValidator(1)]) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = [['cart', 'product']]