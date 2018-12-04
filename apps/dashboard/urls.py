from django.urls import path
from apps.dashboard import views


urlpatterns = [
    path('', views.PanelView.as_view(), name='panel'),
    path('login', views.AuthView.as_view(), name='login'),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('credit', views.CreditView.as_view(), name='credit'),
    path('new-analyze', views.AnalyseFormView.as_view(), name='new-analyze'),
    path('follow-analyze', views.AnalyseView.as_view(), name='follow-analyze'),
]
