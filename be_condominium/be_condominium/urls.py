from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings
#from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from drf_spectacular.views import SpectacularAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ad/', include('modules.ad.urls')),
    path('api/ai/', include('modules.ai_security.urls')),
    path('cn/', include('modules.cn.urls')),

    # Swagger y Redoc
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
]

 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)