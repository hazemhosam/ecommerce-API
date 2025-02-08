from rest_framework import serializers

from customer.models import Customer ,Address

class AdressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id','customer_id','address','city',
                  'state','zip_code']

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    addresses = AdressSerializer(many=True, read_only=True) 
    class Meta:
        model = Customer
        fields = ['id','user_id','phone','birth_date','addresses']
        