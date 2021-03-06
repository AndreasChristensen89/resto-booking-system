from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from .forms import ContactForm, ContactFormLoggedin
from django.contrib.auth.models import User
from restaurant.models import OpeningHours


def contact(request):
    """
    Contact view for submission of form
    """
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
                settings.EMAIL_HOST_USER,
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


def contact_logged_in(request):
    """
    Contact view login for submission of form
    """
    if request.method == 'GET':
        form = ContactFormLoggedin()
    else:
        form = ContactFormLoggedin(request.POST)
        if form.is_valid():
            body = {
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())
            messages.success(request, 'Your message has been sent!')

            send_mail(
                "Dre's Diner",
                'Hello ' + request.user.first_name + ', thank you for getting in touch.' '\n'
                'We received this message from you' ',\n' + form.cleaned_data['message'],
                settings.EMAIL_HOST_USER,
                [request.user.email, 'dresdiner.notice@gmail.com'],
                fail_silently=False
            )

        else:
            messages.error(
                request, "Please correct any errors")
            return render(request, 'contact_login.html', {'form': form})
    form = ContactFormLoggedin()
    opening_list = OpeningHours.objects.all()
    return render(request, "contact_login.html", {'form': form, 'opening_list': opening_list})
