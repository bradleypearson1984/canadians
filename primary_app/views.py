from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Canadian, Snack
from .forms import FeedingForm 


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

class Detail(DetailView):
    model = Canadian
    fields = '__all__'
    template_name = 'canadians/detail.html'


class CanadianCreate(CreateView):
    model = Canadian
    fields = '__all__'
    template_name = 'canadians/canadian_form.html'

class CanadianUpdate(UpdateView):
    model = Canadian
    fields = ('name', 'about', 'hometown')
    template_name = 'canadians/canadian_form.html'

class CanadianDelete(DeleteView):
    model = Canadian
    success_url = '/canadians'
    template_name = 'canadians_canadian_confirm_delete.html'

