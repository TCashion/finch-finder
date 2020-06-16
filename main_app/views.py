from django.shortcuts import render
from .models import Bird

# Create your views here.
def home(request):
    return render(request, 'main_app/home.html')

def birds_index(request):
    birds = Bird.objects.all()
    return render(request, 'birds/index.html', { 'birds': birds })