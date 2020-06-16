from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'main_app/home.html')

def birds_index(request):
    return render(request, 'birds/index.html')