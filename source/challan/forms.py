from django import forms

class NumberPlateForm(forms.Form):
    number_plate = forms.CharField(max_length=20, label='Number Plate')
