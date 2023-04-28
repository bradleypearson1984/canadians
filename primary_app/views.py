from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest

from django.contrib import admin 

from .models import Canadian, Snack, City, Photo, CityPhoto, SnackPhoto
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
    
    #cities they're GOING TO
    # canadian_city_ids = canadian.cities.all().values_list('id')
    #cities they CAN go to
    # cities_canadian_can_go = City.objects.exclude(id__in=canadian_city_ids)
    cities_canadian_can_go = City.objects.exclude(id__in=canadian.cities.all().values_list('id'))
    return render(request, 'canadians/detail.html', {
        'canadian': canadian,
        'cities': cities_canadian_can_go
        })


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
    fields = ('name', 'about', 'hometown', 'quote')
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

@login_required 
def snacks_index(request):
    snacks = Snack.objects.filter(user=request.user)
    return render(request, 'snacks/snacks_index.html', {'snacks': snacks})

@login_required 
def snack_detail(request, snack_id):
    snack = Snack.objects.get(id=snack_id)
    return render(request, 'snacks/snack_detail.html', {'snack': snack})

class SnackCreate(LoginRequiredMixin, CreateView):
    model = Snack
    fields = ('name', 'about')
    template_name = 'snacks/snack_form.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class SnackUpdate(LoginRequiredMixin, UpdateView):
    model = Snack
    fields = '__all__'
    template_name = 'snacks/snack_form.html'

class SnackDelete(LoginRequiredMixin, DeleteView):
    model = Snack
    success_url = '/snacks'
    template_name = 'snacks/snack_confirm_delete.html'






@login_required
def assoc_city(request, canadian_id, city_id):
    canadian = Canadian.objects.get(id=canadian_id)
    canadian.cities.add(city_id)
    return redirect('canadian_detail', canadian_id=canadian_id) 

@login_required
def unassoc_city(request, canadian_id, city_id):
    canadian = Canadian.objects.get(id=canadian_id)
    canadian.cities.remove(city_id)
    return redirect('canadian_detail', canadian_id=canadian_id) 


@login_required
def assoc_snack(request, canadian_id, snack_id):
    canadian = Canadian.objects.get(id=canadian_id)
    canadian.snacks.add(snack_id)
    return redirect('canadian_detail', canadian_id=canadian_id) 

@login_required
def unassoc_snack(request, canadian_id, snack_id):
    canadian = Canadian.objects.get(id=canadian_id)
    canadian.snacks.remove(snack_id)
    return redirect('canadian_detail', canadian_id=canadian_id) 






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
            print('Ope, sorry, photo upload failed, sorry.')
            print(error)
        
        return redirect('canadian_detail', canadian_id=canadian_id)
    
def add_city_photo(request, city_id):
    print('city_id from URL parameter:', city_id)
    city_photo_file = request.FILES.get('city-photo-file', None)

    if city_photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + city_photo_file.name[city_photo_file.name.rfind('.'):]

        try:
            s3.upload_fileobj(city_photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            print(url)

            CityPhoto.objects.create(url=url, city_id=city_id)

        except Exception as error:
            print('Ope, sorry, photo upload failed, sorry.')
            print(error)
        
        return redirect('city_detail', city_id=city_id)
        

def add_snack_photo(request, snack_id):
    print('snack_id from URL parameter:', snack_id)
    snack_photo_file = request.FILES.get('snack-photo-file', None)

    if snack_photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + snack_photo_file.name[snack_photo_file.name.rfind('.'):]

        try:
            s3.upload_fileobj(snack_photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            print(url)

            SnackPhoto.objects.create(url=url, snack_id=snack_id)

        except Exception as error:
            print('Ope, sorry, photo upload failed, sorry.')
            print(error)
        
        return redirect('snack_detail', snack_id=snack_id)