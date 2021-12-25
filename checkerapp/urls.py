from django.urls import path, include
from . import views
app_name = 'checkerapp'

urlpatterns = [
    path('', views.CallistaDataFileCreateView.as_view(), name='upload'),
    # path('success/', views.SuccessView.as_view(), name='success'),
    path('processor/', views.processor, name='processor'),
    path('validator/', views.validator, name='validator'),
]
