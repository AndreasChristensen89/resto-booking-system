from django.shortcuts import render
from django.views import View
# from reservations.forms import DateAndGuestsForm
from django.http import HttpResponseRedirect

# Create your views here.


def index(request):

    return render(request, 'index.html')
