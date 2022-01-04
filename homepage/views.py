from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect


def index(request):
    return render(request, 'index.html')


def custom_page_not_found_view(request, exception):
    return render(request, "404.html", {})
