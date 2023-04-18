from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('canadians/', views.canadians_index, name='canadians_index'),
    path('canadians/<int:canadian_id>', views.canadians_detail, name='canadians_detail'),

]