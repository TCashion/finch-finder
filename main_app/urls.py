from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('birds/', views.birds_index, name='birds_index'),
    path('birds/<int:bird_id>/', views.birds_detail, name='birds_detail'),
    path('birds/create/', views.BirdCreate.as_view(), name='birds_create'),
    path('birds/<int:pk>/update/', views.BirdUpdate.as_view(), name='birds_update'),
    path('birds/<int:pk>/delete/', views.BirdDelete.as_view(), name='birds_delete'),
    path('birds/<int:pk>/add_sighting', views.add_sighting, name='add_sighting')
]
