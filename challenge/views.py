from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, 'home/index.html')
    else:
        redirect('login')
