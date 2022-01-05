from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('no_user/', views.contact, name='contact'),
    path('login/', views.contact_logged_in, name='contact_login'),
]