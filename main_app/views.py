from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'main_app/home.html')

def finches_index(request):
    return render(request, 'finches/index.html')