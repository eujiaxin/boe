from django.urls import path, include
from . import views
app_name = 'checkerapp'

urlpatterns = [
    path('upload/', views.CallistaDataFileCreateView.as_view(), name='upload'),
    # path('success/', views.SuccessView.as_view(), name='success'),
    path('processor/', views.processer, name='processer'),
]
