from django.urls import path, include
from apps.site import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('how-it-works', views.HowItWorksView.as_view(), name='how-it-works'),
    path('step-1', views.Step1View.as_view(), name='step-1'),
    path('step-2', views.Step2View.as_view(), name='step-2'),
    path('step-3', views.Step3View.as_view(), name='step-3'),
    path('plans', views.PlansView.as_view(), name='plans'),
    path('example', views.ExampleView.as_view(), name='example'),
]
