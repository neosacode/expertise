from django.urls import path
from apps.dashboard.views import PanelView, AuthView, LogoutView


urlpatterns = [
    path('', PanelView.as_view(), name='panel'),
    path('login', AuthView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
