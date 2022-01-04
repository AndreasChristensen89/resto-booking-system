from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages
from .forms import ContactForm
from restaurant.models import OpeningHours


def contact(request):
    """Contactemail app view for submission of form"""
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            body = {
                'message': form.cleaned_data['message'],
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email_address']
            }
            message = "\n".join(body.values())
            messages.success(request, 'Your message has been sent!')

            send_mail(
                "Dre's Diner",
                'Hello ' + form.cleaned_data['name'] + ', thank you for getting in touch.' '\n'
                'We received this message from you' ',\n' + form.cleaned_data['message'],
                None,
                [form.cleaned_data['email_address'], 'dresdiner.notice@gmail.com'],
                fail_silently=False
            )
            
        else:
            messages.error(
                request, "Please correct any errors")
            return render(request, 'contact.html', {'form': form})
    form = ContactForm()
    opening_list = OpeningHours.objects.all()
    return render(request, "contact.html", {'form': form, 'opening_list': opening_list})
