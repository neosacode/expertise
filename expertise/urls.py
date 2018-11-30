from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('apps.site.urls', 'site'), namespace='site')),
    path('dashboard/', include(('apps.dashboard.urls', 'dashboard'), namespace='dashboard')),
]
