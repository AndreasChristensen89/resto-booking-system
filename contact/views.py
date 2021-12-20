from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib import messages
from .forms import ContactForm


def contact(request):
    """Contactemail app view for submission of form"""
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Enquiry"
            body = {
                'message': form.cleaned_data['message'],
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email_address']
            }
            message = "\n".join(body.values())
            messages.success(request, 'Message sent successfully!')

            try:
                send_mail(subject, message, 'dresdiner@email.com', [
                    'dresdiner@email.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header.')
        else:
            messages.error(
                request, "Please correct any errors")
            return render(request, 'contact.html', {'form': form})
    form = ContactForm()
    return render(request, "contact.html", {'form': form})

