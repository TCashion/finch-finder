from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('birds/', views.birds_index, name='birds_index'),
    path('birds/<int:bird_id>/', views.birds_detail, name='birds_detail'),
    path('birds/create/', views.BirdCreate.as_view(), name='birds_create'),
    path('birds/<int:pk>/update/', views.BirdUpdate.as_view(), name='birds_update'),
    path('birds/<int:pk>/delete/', views.BirdDelete.as_view(), name='birds_delete'),
    path('birds/<int:bird_id>/add_sighting', views.add_sighting, name='add_sighting'),
    path('locations/', views.locations_index, name='locations_index'),
    path('locations/create/', views.LocationCreate.as_view(), name='locations_create'),
    path('locations/<int:pk>/', views.LocationDetail.as_view(), name='locations_detail'),
    path('locations/<int:pk>/delete/', views.LocationDelete.as_view(), name='locations_delete')    
]
