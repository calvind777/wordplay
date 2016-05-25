from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.template.loader import render_to_string

def home(request):
    homepage = loader.get_template('search/home.html')
    
    return HttpResponse(homepage.render(request))



# Create your views here.
