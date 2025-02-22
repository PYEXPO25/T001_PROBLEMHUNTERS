from django.urls import path, include

from . import views

urlpatterns = [
    path('upload/', upload_violation, name='upload_violation'),  # Add path for uploading violations

    path('violation/', views.violation_view, name='violation'),
    path('add/',views.test_add,name='test_add'),
]
