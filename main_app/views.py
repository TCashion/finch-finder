from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Bird
from .forms import SightingForm


# Create your views here.
def home(request):
    return render(request, 'home.html')


def birds_index(request):
    birds = Bird.objects.all()
    return render(request, 'birds/index.html', { 'birds': birds })


def birds_detail(request, bird_id):
    bird = Bird.objects.get(id=bird_id)
    sighting_form = SightingForm()
    return render(request, 'birds/detail.html', { 
        'bird': bird, 
        'sighting_form': sighting_form
    })


def add_sighting(request, bird_id):
    pass

class BirdCreate(CreateView):
    model = Bird
    fields = '__all__'


class BirdUpdate(UpdateView):
    model = Bird
    fields = '__all__'


class BirdDelete(DeleteView):
    model = Bird
    success_url = '/birds/'