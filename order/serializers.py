from rest_framework import serializers
from django.db import transaction

from cart.models import Cart, CartItem
from customer.models import Customer
from order.models import Order, OrderItem 
from cart.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer() 
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ['id','product','quantity','total_price'] 

    def get_total_price(self,obj):
        return obj.product.price * obj.quantity    

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ['id','customer','placed_at','status','items','total_price']
    def get_total_price(self,obj):
        return sum([item.product.price * item.quantity 
                    for item in obj.items.all()])    

class OrderCreateSerializer(serializers.Serializer):
   cart_id = serializers.UUIDField() 
   def save(self, **kwargs):
        with transaction.atomic():
            user_id = self.context['user_id'] 
            customer= Customer.objects.get(user_id=user_id) 
            order =Order.objects.create(customer=customer) 
            cart_items = CartItem.objects.\
                    select_related('product').\
                    filter(cart_id=self.validated_data['cart_id'])
            order_item =[OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
            )for item in cart_items]
            OrderItem.objects.bulk_create(order_item) 
            Cart.objects.get(pk=self.validated_data['cart_id']).delete() 

            return order
        
class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']
        

