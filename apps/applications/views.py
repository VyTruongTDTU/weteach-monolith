from django.shortcuts import render

# Create your views here.
def index(request):
    # Example view function
    return render(request, 'base.html')