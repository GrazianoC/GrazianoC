from django.shortcuts import render
# Create your models here.

def home_view(request):
     
     return render(request, "home/index.html")
