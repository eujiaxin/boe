from django.urls import path, include
from . import views
appname = 'checkerapp'

urlpatterns = [
    path('upload/', views.CallistaDataFileCreateView.as_view(), name='upload'),
    path('success/', views.success, name='success'),
]
