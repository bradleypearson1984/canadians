from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Canadian, Snack, City
# from .forms import FeedingForm 


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def canadians_index(request):
    canadians = Canadian.objects.filter(user=request.user)
    return render(request, 'canadians/index.html', {'canadians': canadians})

def canadian_detail(request, canadian_id):
    canadian = Canadian.objects.get(id=canadian_id)
    return render(request, 'canadians/detail.html', {'canadian': canadian})


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

def cities_index(request):
    cities = City.objects.filter(user=request.user)
    return render(request, 'cities/cities_index.html', {'cities': cities})

def city_detail(request, city_id):
    city = City.objects.get(id=city_id)
    return render(request, 'cities/city_detail.html', {'city': city})

class CityCreate(CreateView):
    model = City
    fields = '__all__'
    template_name = 'cities/city_form.html'

class CityUpdate(UpdateView):
    model = City
    fields = '__all__'
    template_name = 'cities/city_form.html'

class CityDelete(DeleteView):
    model = City
    success_url = '/cities'
    template_name = 'cities_city_confirm_delete.html'

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
            # redirect to the cats index page 
            return redirect('writers_index')
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
