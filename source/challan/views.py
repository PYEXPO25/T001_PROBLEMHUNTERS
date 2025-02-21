from django.shortcuts import render
from django.http import HttpResponse
from .models import Violation

def violation_view(request):
    
    violations = Violation.objects.all().order_by('-violation_time')
    return render(request, 'challan/violation.html', {'violations': violations})
    
def test_add(request):
    
    return HttpResponse('Violation Added')