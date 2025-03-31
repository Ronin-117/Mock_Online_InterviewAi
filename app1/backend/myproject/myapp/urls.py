# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('data/', views.get_data, name='get_data'),
    path('speak/', views.speak_text, name='speak_text'), # Assuming you have this already
]