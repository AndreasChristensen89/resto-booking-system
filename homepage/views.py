from django.shortcuts import render
from django.views import View

# Create your views here.


def index(request):
    return render(request,'index.html')
