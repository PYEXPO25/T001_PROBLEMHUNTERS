from django import forms

class NumberPlateForm(forms.Form):
    number_plate = forms.CharField(max_length=20, label='Number Plate')

class PathForm(forms.Form):
    path = forms.CharField(max_length=200, label='Video URL')