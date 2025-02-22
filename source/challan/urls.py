from django.urls import path
from . import views

urlpatterns = [
    path('', views.input_number_plate, name='input_number_plate'),  # Add path for inputting number plate
    path('violation/', views.violation_list, name='violation'),  # Ensure this matches the view name
]
