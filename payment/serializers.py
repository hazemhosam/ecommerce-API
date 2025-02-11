from rest_framework import serializers

from order.models import Order 

class PaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

    def validate_order_id(self, value):
        # Check if the order exists
        if not Order.objects.filter(id=value).exists():
            raise serializers.ValidationError('order not found')
        return value  
