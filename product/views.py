from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet 
from . serializers import ProductSerializer,ReviewSerializer
from django.db.models.aggregates import Count ,Sum,Avg
from .models import Product ,ProductReview

# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('reviews')\
        .select_related('category')\
        .annotate(
        rating=Avg('reviews__rating')).all() 
    serializer_class = ProductSerializer 

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return ProductReview.objects.filter(product_id=self.kwargs['product_pk'])
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']} 