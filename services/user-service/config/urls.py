from django.http import JsonResponse
from django.contrib import admin
from django.urls import path, include

def health_check(request):
    return JsonResponse({'status': 'healthy', 'service': 'user_service'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/users/', include('apps.users.urls')),
]

