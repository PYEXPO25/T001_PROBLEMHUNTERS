from django.urls import path
from . import views

urlpatterns = [
    path('', views.input_number_plate, name='input_number_plate'), 
    
]
