from rest_framework import serializers 
from .models import Product, ProductReview 

class ProductSerializer(serializers.ModelSerializer): 
    rating = serializers.FloatField(read_only=True) 
    category = serializers.SerializerMethodField()
    class Meta: 
        model = Product 
        fields = ['id', 'title', 'description', 'price',
        'inventory','rating' ,'category'] 

    def get_category(self, obj):
        return obj.category.title if obj.category else None    
        

class ReviewSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = ProductReview 
        fields = ['id','name','date','rating', 'review']
        

    def create(self, validated_data):
        validated_data['product_id'] = self.context['product_id']
        return super().create(validated_data)    

