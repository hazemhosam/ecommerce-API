from rest_framework import serializers

from cart.models import Cart, CartItem
from product.models import Product

class ProductSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title','description','price']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSimpleSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id','product','quantity','total_price']

    def get_total_price(self,obj):
        return obj.product.price * obj.quantity  

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id','items','total_price']

    def get_total_price(self,obj):
        return sum([item.product.price * item.quantity 
                    for item in obj.items.all()])
    
class CartItemCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = CartItem
        fields = ['id','product_id','quantity']

    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError('Product not found')
        return value  

    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity'] 
        cart_id = self.context['cart_id'] 
        cart = Cart.objects.get(id=cart_id) 
        if cart.items.filter(product_id=product_id).exists():
            item = cart.items.get(product_id=product_id)
            item.quantity += quantity
            item.save()
            self.instance = item 
            return self.instance
        else:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance 

class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity'] 
        