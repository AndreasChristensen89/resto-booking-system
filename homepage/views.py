from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect


def index(request):
    return render(request, 'index.html')
