from rest_framework_nested import routers 
from product import views 
from category import views as category_views



router = routers.DefaultRouter() 
router.register('products', views.ProductViewSet,
                 basename='products')
router.register('categories', category_views.CategoryViewSet,
                 basename='categories')

product_router = routers.NestedDefaultRouter(router, 'products',
                                             lookup='product')
product_router.register('reviews', views.ReviewViewSet, 
                        basename='product-reviews') 

urlpatterns = router.urls + product_router.urls
