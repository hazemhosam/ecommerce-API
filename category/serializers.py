from rest_framework import serializers 
from .models import Category

class CategorySerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Category 
        fields = ['id', 'title', 'description','product_count']
    product_count = serializers.IntegerField(read_only=True)