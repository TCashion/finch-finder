from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Bird, Location, Sighting, BirdPhoto, LocationPhoto
from .forms import SightingForm
import uuid
import boto3


# configure AWS3 server and BUCKET
S3_BASE_URL = 'https://s3.us-west-1.amazonaws.com/'
BUCKET = 'finchfinder'


# Create your views here.
def home(request):
    return render(request, 'home.html')


@login_required
def birds_index(request):
    birds = Bird.objects.filter(user=request.user)
    return render(request, 'birds/index.html', {'birds': birds})


@login_required
def birds_detail(request, bird_id):
    bird = Bird.objects.get(id=bird_id)
    unassoc_locations = Location.objects.exclude(id__in=bird.locations.all().values_list('id')).filter(user=request.user)
    sighting_form = SightingForm()
    return render(request, 'birds/detail.html', {
        'bird': bird,
        'sighting_form': sighting_form,
        'locations': unassoc_locations,
    })


@login_required
def add_sighting(request, bird_id):
    form = SightingForm(request.POST)
    if form.is_valid():
        new_sighting = form.save(commit=False)
        new_sighting.bird_id = bird_id
        new_sighting.save()
    return redirect('birds_detail', bird_id=bird_id)


@login_required
def delete_sighting(request, bird_id, sighting_id):
    s = Sighting.objects.get(id=sighting_id)
    s.delete()
    return redirect('birds_detail', bird_id=bird_id)


@login_required
def locations_index(request):
    locations = Location.objects.filter(user=request.user)
    return render(request, 'locations/index.html', {'locations': locations})


@login_required
def locations_detail(request, location_id):
    birds = Bird.objects.filter(user=request.user)
    location = Location.objects.get(id=location_id)
    return render(request, 'locations/detail.html', {
        'location': location,
        'birds': birds
    })


@login_required
def assoc_location(request, bird_id, location_id):
    Bird.objects.get(id=bird_id).locations.add(location_id)
    return redirect('birds_detail', bird_id=bird_id)


@login_required
def disassoc_location(request, bird_id, location_id):
    Bird.objects.get(id=bird_id).locations.remove(location_id)
    return redirect('birds_detail', bird_id=bird_id)


@login_required
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


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('birds_index')
        else:
            error_message = 'Invalid sign up = try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


class BirdCreate(LoginRequiredMixin, CreateView):
    model = Bird
    fields = ['name', 'scientific_name', 'description', 'invasive']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BirdUpdate(LoginRequiredMixin, UpdateView):
    model = Bird
    fields = ['name', 'scientific_name', 'description', 'invasive']


class BirdDelete(LoginRequiredMixin, DeleteView):
    model = Bird
    success_url = '/birds/'


class LocationCreate(LoginRequiredMixin, CreateView):
    model = Location
    fields = ['name', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class LocationDelete(LoginRequiredMixin, DeleteView):
    model = Location
    success_url = '/locations/'


class LocationUpdate(LoginRequiredMixin, UpdateView):
    model = Location
    fields = '__all__'
