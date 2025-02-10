from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet 
from django.db.models.aggregates import Count   
from . models import Category 
from .serializers import CategorySerializer
from product.permissions import IsAdminOrReadOnly
# Create your views here.
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
        product_count=Count('products')).all() 
    serializer_class = CategorySerializer 
    permission_classes = [IsAdminOrReadOnly] 

    

    
