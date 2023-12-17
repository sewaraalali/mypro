from rest_framework import serializers 
from . models import *

class  MovieSerializers(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields =['hall','movie','date']



class  ResverationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Resveration
        fields =['guest','movie']



class  GuestSerializers(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields =['pk','reservation','name','mobile']


class  PostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields ='__all__'