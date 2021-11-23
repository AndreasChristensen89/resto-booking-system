from django.shortcuts import render
from django.views import View
from bookings.forms import DateAndGuestsForm
from django.http import HttpResponseRedirect

# Create your views here.


def index(request):
    form = DateAndGuestsForm()
    if request.method == 'POST':
        form = DateAndGuestsForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/bookings/book_table/')
        else:
            form = DateAndGuestsForm()

    return render(request, 'index.html', {'form': form})
