# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('start_interview/', views.start_interview, name='start_interview'),  # Make sure to create the function
]