from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Guest)
class GusetAdmin(admin.ModelAdmin):
    list_display =['id','name','mobile']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display =['hall','movie','date']



admin.site.register(Post)
admin.site.register(Resveration)
