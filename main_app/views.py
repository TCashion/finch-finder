from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Bird, Location
from .forms import SightingForm


# Create your views here.
def home(request):
    return render(request, 'home.html')


def birds_index(request):
    birds = Bird.objects.all()
    return render(request, 'birds/index.html', { 'birds': birds })


def birds_detail(request, bird_id):
    bird = Bird.objects.get(id=bird_id)
    unassoc_locations = Location.objects.exclude(id__in = bird.locations.all().values_list('id'))
    sighting_form = SightingForm()
    return render(request, 'birds/detail.html', { 
        'bird': bird, 
        'sighting_form': sighting_form, 
        'locations': unassoc_locations,
    })


def add_sighting(request, bird_id):
    form = SightingForm(request.POST)
    if form.is_valid():
        new_sighting = form.save(commit=False)
        new_sighting.bird_id = bird_id
        new_sighting.save()
    return redirect('birds_detail', bird_id=bird_id)


def locations_index(request):
    locations = Location.objects.all()
    return render(request, 'locations/index.html', { 'locations' : locations })


def locations_detail(request, location_id):
    location = Location.objects.get(id=location_id)
    return render(request, 'locations/detail.html', {'location': location})


def assoc_location(request, bird_id, location_id):
    Bird.objects.get(id=bird_id).locations.add(location_id)
    return redirect('birds_detail', bird_id=bird_id)


class BirdCreate(CreateView):
    model = Bird
    fields = '__all__'


class BirdUpdate(UpdateView):
    model = Bird
    fields = '__all__'


class BirdDelete(DeleteView):
    model = Bird
    success_url = '/birds/'


class LocationCreate(CreateView):
    model = Location
    fields = '__all__'


class LocationDelete(DeleteView):
    model = Location
    success_url = '/locations/'


class LocationUpdate(UpdateView):
    model = Location
    fields = '__all__'