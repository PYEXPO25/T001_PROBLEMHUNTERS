from django.shortcuts import render, redirect
from .forms import ViolationForm
from .models import Violation

def upload_violation(request):
    if request.method == 'POST':
        form = ViolationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the violation instance
            return redirect('violation_list')  # Redirect to the list of violations
    else:
        form = ViolationForm()
    return render(request, 'challan/upload_violation.html', {'form': form})

def violation_list(request):
    violations = Violation.objects.all()
    return render(request, 'challan/violation.html', {'violations': violations})
