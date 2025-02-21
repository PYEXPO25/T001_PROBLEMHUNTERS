from django.urls import path
from . import views

urlpatterns = [
    path('violation/', views.violation_view, name='violation'),
    path('',views.test_add,name='test_add'),
]
