from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact, name='contact_logout'),
    path('login/', views.contact_logged_in, name='contact_login'),
]