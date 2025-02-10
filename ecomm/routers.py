from rest_framework_nested import routers 
from product import views 
from category import views as category_views
from customer import views as customer_views
from cart import views as cart_views 
from order import views as order_views




router = routers.DefaultRouter() 
router.register('products', views.ProductViewSet,
                 basename='products')
router.register('categories', category_views.CategoryViewSet,
                 basename='categories')
router.register('customers', customer_views.CustomerVeiwSet,
                 basename='customers')
router.register('carts', cart_views.CartViewSet,
                basename='carts')
router.register('orders', order_views.OrderViewSet,
                basename='orders')

product_router = routers.NestedDefaultRouter(router, 'products',
                                             lookup='product')
product_router.register('reviews', views.ReviewViewSet, 
                        basename='product-reviews')

cart_router = routers.NestedDefaultRouter(router, 'carts',
                                                lookup='cart')
cart_router.register('items', cart_views.CartItemViewSet,
                        basename='cart-items') 

urlpatterns = router.urls + product_router.urls + cart_router.urls
