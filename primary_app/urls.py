from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    
    path('canadians/', views.canadians_index, name='canadians_index'),
    path('canadians/<int:canadian_id>', views.canadian_detail, name='canadian_detail'),
    path('canadians/create/', views.CanadianCreate.as_view(), name='canadian_create'),
    path('canadians/<int:pk>/update/', views.CanadianUpdate.as_view(), name='canadian_update'),
    path('canadians/<int:pk>/delete/', views.CanadianDelete.as_view(), name='canadian_delete'),

    path('cities/', views.cities_index, name='cities_index'),
    path('cities/<int:city_id>/detail', views.city_detail, name='city_detail'),
    path('cities/create', views.CityCreate.as_view(), name='city_create'),
    path('cities/<int:pk>/update', views.CityUpdate.as_view(), name='city_update'),
    path('cities/<int:pk>/delete', views.CityDelete.as_view(), name='city_delete'),

    path('accounts/signup', views.signup, name='signup'),
    path('canadians/<int:canadian_id>/add_photo/', views.add_photo, name='add_photo'),
]
