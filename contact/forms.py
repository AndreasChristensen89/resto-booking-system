from django import forms


class ContactForm(forms.Form):
    """
    Contact email form
    """
    name = forms.CharField(required=True)
    email_address = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class ContactFormLoggedin(forms.Form):
    """
    Contact email form logged in
    """
    message = forms.CharField(widget=forms.Textarea, required=True)
