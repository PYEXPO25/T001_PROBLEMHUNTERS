from django import forms
from .models import Violation

class ViolationForm(forms.ModelForm):
    class Meta:
        model = Violation
        fields = ['number_plate', 'violation_time', 'fine_amount', 'image']  # Corrected field name

    class Meta:
        model = Violation
        fields = ['number_plate', 'violation_time', 'fine_amount', 'image_directory']  # Include fields as needed
