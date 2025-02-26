from django.urls import path
from . import views

urlpatterns = [
    path('', views.input_number_plate, name='input_number_plate'), 
    
    path('path/', views.path_view, name='input_video_url'),    
]

