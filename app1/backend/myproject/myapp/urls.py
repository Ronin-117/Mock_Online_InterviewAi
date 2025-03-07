# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('speak/', views.speak_text, name='speak_text'),  # Make sure to create the function
]