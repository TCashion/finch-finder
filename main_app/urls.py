from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('finches/', views.finches_index, name='index')
]