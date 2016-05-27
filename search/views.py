from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.template.loader import render_to_string
from .forms import SongForm
from django.http import HttpResponseRedirect
from django.template import Context, Template

def home(request):
    
    
    return render(request, 'search/home.html')

def confirm(request):
    if request.method == 'POST':

        form = SongForm(request.POST)
        if form.is_valid():
            print("2")
            return render(request,'search/confirm.html', context = form.cleaned_data)
        print(form.errors)
    return render(request, 'search/confirm.html')

# Create your views here.
