"""
URL configuration for ecomm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static  
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views 
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title= 'E-commerce API',
        default_version='v1',
        description='API documentation for e-comm'
    ),
    public=True,
    authentication_classes=(JWTAuthentication,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ecomm.routers')),
    path('auth/', include('djoser.urls')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),   
    path('payment/', include('payment.urls')),
    path('api/swagger/',schema_view.with_ui('swagger',cache_timeout=0),
         name='schema-swagger-ui')     
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
