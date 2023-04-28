from django.contrib import admin
from .models import Canadian, City, Snack, Photo, CityPhoto, SnackPhoto

admin.site.register(Canadian)
admin.site.register(City)
admin.site.register(Snack)
admin.site.register(Photo)
admin.site.register(CityPhoto)
admin.site.register(SnackPhoto)

# Register your models here.
