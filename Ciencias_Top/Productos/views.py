from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def inicioAdmin(request):
    return render(request, 'inicioV\inicioAdmin.html')


