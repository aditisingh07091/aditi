import requests
from rest_framework import viewsets
from django.shortcuts import render

# Create your views here.

def Home(request):
    response = requests.get('http://127.0.0.1:8000/posts')
    data = response.json()
    return render(request,'home.html',{'data': data})