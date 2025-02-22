from django.shortcuts import render, redirect

from .models import Violation
from .forms import NumberPlateForm


def input_number_plate(request):
    number_plate_form = NumberPlateForm()  

    if request.method == 'POST':
        number_plate_form = NumberPlateForm(request.POST)
        if number_plate_form.is_valid():
            number_plate = number_plate_form.cleaned_data['number_plate']
            # Fetch details from the challan_violations table based on the number plate
            violations = Violation.objects.filter(number_plate=number_plate)  
            return render(request, 'challan/violation.html', {'violations': violations}) 

    return render(request, 'challan/input_number_plate.html', {'number_plate_form': number_plate_form})




