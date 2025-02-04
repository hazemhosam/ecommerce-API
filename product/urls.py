from django.urls import include, path
from rest_framework_nested import routers 
from . import views 



router = routers.DefaultRouter() 
router.register('products', views.ProductViewSet,
                 basename='products')

product_router = routers.NestedDefaultRouter(router, 'products',
                                             lookup='product')
product_router.register('reviews', views.ReviewViewSet, 
                        basename='product-reviews')

urlpatterns = [  # Include category app URLs
    path('', include(router.urls)),  # Include API routes from main router
    path('', include(product_router.urls)),
    path('', include('category.urls')),  # Include API routes from product router
]
