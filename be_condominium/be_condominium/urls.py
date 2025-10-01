from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

# Health check endpoint
def health_check(request):
    return JsonResponse({
        "status": "healthy",
        "service": "Condominium Backend API",
        "version": "1.0.0"
    }, status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ad/', include('modules.ad.urls')),
    path('api/ai/', include('modules.ai_security.urls')),
    path('cn/', include('modules.cn.urls')),

    # Health check
    path('health/', health_check, name='health-check'),
    
    # Swagger y Redoc
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)