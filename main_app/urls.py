from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('birds/', views.birds_index, name='birds_index'),
    path('birds/<int:bird_id>/', views.birds_detail, name='detail'),
]
