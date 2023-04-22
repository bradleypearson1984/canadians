from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Canadian, Snack, City, Photo
from django.contrib.auth.forms import UserCreationForm
# from .forms import FeedingForm 

import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'canadians1108'


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required 
def canadians_index(request):
    canadians = Canadian.objects.filter(user=request.user)
    return render(request, 'canadians/index.html', {'canadians': canadians})

@login_required 
def canadian_detail(request, canadian_id):
    canadian = Canadian.objects.get(id=canadian_id)
    return render(request, 'canadians/detail.html', {'canadian': canadian})

# def add_photo(request, canadian_id):
#     pass 

class CanadianCreate(LoginRequiredMixin, CreateView):
    model = Canadian
    fields = ('name', 'age', 'hometown', 'about', 'quote')
    template_name = 'canadians/canadian_form.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CanadianUpdate(LoginRequiredMixin, UpdateView):
    model = Canadian
    fields = ('name', 'about', 'hometown')
    template_name = 'canadians/canadian_form.html'

class CanadianDelete(LoginRequiredMixin, DeleteView):
    model = Canadian
    success_url = '/canadians'
    template_name = 'canadians/canadian_confirm_delete.html'

@login_required 
def cities_index(request):
    cities = City.objects.filter(user=request.user)
    return render(request, 'cities/cities_index.html', {'cities': cities})

@login_required 
def city_detail(request, city_id):
    city = City.objects.get(id=city_id)
    return render(request, 'cities/city_detail.html', {'city': city})

class CityCreate(LoginRequiredMixin, CreateView):
    model = City
    fields = ('name', 'province')
    template_name = 'cities/city_form.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CityUpdate(LoginRequiredMixin, UpdateView):
    model = City
    fields = '__all__'
    template_name = 'cities/city_form.html'

class CityDelete(LoginRequiredMixin, DeleteView):
    model = City
    success_url = '/cities'
    template_name = 'cities/city_confirm_delete.html'

def signup(request):
    #POST requests
    error_message = ''
    if request.method == 'POST':

        # create user  using the UserCreationForm 
        # this way we can validate form inputs 
        form = UserCreationForm(request.POST)
        # check if the form inputs are valid
        if form.is_valid():
        # if valid: save new user to db 
            user = form.save()
            # login the new user 
            login(request, user)
         
            return redirect('canadians_index')
        # else: generate error message 'invalid input'
        else:
            error_message = "Sorry, invalid signup, I'm sure I'm sorry"
            #redirect back to signup 

    #GET requests
        # send an empty form to the client 
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form, 
        'error': error_message
        })

def add_photo(request, canadian_id):
    photo_file = request.FILES.get('photo-file', None)

    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]

        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"

            Photo.objects.create(url=url, canadian_id=canadian_id)

        except Exception as error:
            print('Sorry, photo upload failed, sorry.')
            print(error)
        
        return redirect('canadian_detail', canadian_id=canadian_id)
    
