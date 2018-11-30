from django.urls import path, include
from apps.site.views import HomeView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
