# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('start_interview/', views.start_interview, name='start_interview'), 
    path('start_non_verbal_interview/', views.start_non_verbal_interview, name='start_non_verbal_interview'),
    path('get_data/',views.get_data, name="get_data") ,
    
]   