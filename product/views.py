from rest_framework.viewsets import ModelViewSet 
from rest_framework import permissions 
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from pagination.pagination import DefaultPagination
from . serializers import ProductSerializer,ReviewSerializer
from django.db.models.aggregates import Avg
from .models import Product ,ProductReview
from .permissions import IsAdminOrReadOnly
from .filters import ProductFilter

# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related('reviews')\
        .select_related('category')\
        .annotate(
        rating=Avg('reviews__rating')).all() 
    serializer_class = ProductSerializer 
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_class = ProductFilter 
    search_fields = ['title','description']
    pagination_class = DefaultPagination


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

    def get_queryset(self):
        return ProductReview.objects. \
            filter(product_id=self.kwargs['product_pk'])
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']} 