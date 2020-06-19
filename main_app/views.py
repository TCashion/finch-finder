from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Bird, Location, Sighting, BirdPhoto, LocationPhoto
from .forms import SightingForm
import uuid
import boto3


# configure AWS3 BUCKET
S3_BASE_URL = 'https://s3.us-west-1.amazonaws.com/'
BUCKET = 'finchfinder'


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


def delete_sighting(request, bird_id, sighting_id):
    s = Sighting.objects.get(id=sighting_id)
    s.delete()
    return redirect('birds_detail', bird_id=bird_id)


def locations_index(request):
    locations = Location.objects.all()
    return render(request, 'locations/index.html', { 'locations' : locations })


def locations_detail(request, location_id):
    birds = Bird.objects.all()
    location = Location.objects.get(id=location_id)
    return render(request, 'locations/detail.html', {
        'location': location, 
        'birds': birds
    })


def assoc_location(request, bird_id, location_id):
    Bird.objects.get(id=bird_id).locations.add(location_id)
    return redirect('birds_detail', bird_id=bird_id)


def disassoc_location(request, bird_id, location_id):
    Bird.objects.get(id=bird_id).locations.remove(location_id)
    return redirect('birds_detail', bird_id=bird_id)


def add_photo(request, bird_id, location_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            if bird_id > 0:
                photo = BirdPhoto(url=url, bird_id=bird_id)
            elif location_id > 0:
                photo = LocationPhoto(url=url, location_id=location_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    if bird_id > 0:
        return redirect('birds_detail', bird_id=bird_id)
    elif location_id > 0:
        return redirect('locations_detail', location_id=location_id)


class BirdCreate(CreateView):
    model = Bird
    fields = '__all__'


class BirdUpdate(UpdateView):
    model = Bird
    fields = ['name', 'scientific_name', 'description', 'invasive']


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