from rest_framework_nested import routers 
from . import views 



router = routers.DefaultRouter() 
router.register('categories', views.CategoryViewSet,
                 basename='categories')

urlpatterns = router.urls 