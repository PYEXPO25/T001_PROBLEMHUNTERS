from django.shortcuts import render, redirect
import subprocess
from .models import Violation
from .forms import NumberPlateForm,PathForm
from django.http import HttpResponse
import subprocess
import os


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



def path_view(request):
    if request.method == 'POST':
        form = PathForm(request.POST)
        if form.is_valid():
            path = form.cleaned_data['path']
            script_dir = r"E:\Python Projects\attempt1\archive\script"
            venv_python = r"E:\Python Projects\attempt1\archive\myenv\Scripts\python.exe"
            extract_script = os.path.join(script_dir, "extract_plate.py")

            try:
                # **Run the script with the virtual environment's Python**
                result = subprocess.run(
                    [venv_python, extract_script, path],
                    capture_output=True, text=True, check=True
                )

                # **Check output for debugging**
                print(f"📌 DEBUG: Subprocess Output → {result.stdout}")
                print(f"📌 DEBUG: Subprocess Error → {result.stderr}")

                # **Ensure the text file exists before reading**
                file_path = r"E:\Python Projects\attempt1\archive\script\output\plate_value.txt"

                if not os.path.exists(file_path):
                    return HttpResponse("❌ Error: Plate value file not found!", status=400)

                # **Read the plate number from the text file**
                with open(file_path, "r") as file:
                    plate_value = file.read().strip()

                print(f"📌 DEBUG: Read plate number → {plate_value}")

                # **Ensure plate_value is not empty**
                if not plate_value:
                    return HttpResponse("❌ Error: No plate number detected!", status=400)

                # **Insert the data into the database**
                violation = Violation.objects.create(
                    number_plate=plate_value,
                    fine_amount=1000,
                    image="rider.jpg",
                    status='Not Paid'
                )

                print(f"📌 DEBUG: Inserted into DB → {violation.number_plate}")

                return HttpResponse(f"✅ Violation recorded: {violation.number_plate} with fine ₹{violation.fine_amount}")

            except subprocess.CalledProcessError as e:
                return HttpResponse(f"❌ Subprocess Error: {e.stderr}", status=500)

            except Exception as e:
                return HttpResponse(f"❌ Error: {str(e)}", status=500)

    else:
        form = PathForm()

    return render(request, 'challan/path.html', {'form': form})




