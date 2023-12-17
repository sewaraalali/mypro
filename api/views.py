from django.shortcuts import render
from .serializers import *
from .models import *
from django.http.response import HttpResponse,JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status ,filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics , mixins ,viewsets
from rest_framework.authentication import BasicAuthentication ,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly

#1 function based view 
#1.1 GET POST
@api_view(['GET','POST'])
def FBV_list(request):
    if request.method == 'GET':
        guests=Guest.objects.all()
        serializer= GuestSerializers(guests,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer =GuestSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data ,status = status.HTTP_201_CREATED)  
        return Response(serializer.data ,status = status.HTTP_400_BAD_REQUEST)  
          

#1.2 PUT DELETE GET    
@api_view(['PUT','DELETE','GET'])
def FBV_pk(request,pk):
    try:
        guests=Guest.objects.get(pk=pk)
    except Guest.DoesNotExists:
        return Response(status =status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer= GuestSerializers(guests)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer =GuestSerializers(guests,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)  
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        guests.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  



#2 CBV CLASS BASED VIEWS
#2.1  list and create = Get and Post

class CBV_list(APIView):
    def get(self,request):
        guests =Guest.objects.all()
        serializer =GuestSerializers(guests,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer =GuestSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data ,status = status.HTTP_201_CREATED)  
        return Response(serializer.data ,status = status.HTTP_400_BAD_REQUEST) 

#2.2 PUT DELETE GET
class CBV_PK(APIView):
    def get_object(self,pk):
        #try:
            guests=Guest.objects.get(pk=pk)
       # except Guest.DoesNotExists:
            #return Response(status =status.HTTP_404_NOT_FOUND)


    def get(self, request, pk):
        guests=self.get_object(pk)
        serializer = GuestSerializers(guests)
        return Response(serializer.data)
  
    def put(self, request, pk):
        guests=self.get_object(pk)
        serializer = GuestSerializers(guests,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data ,status = status.HTTP_201_CREATED)  
        return Response(serializer.data ,status = status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, pk):
        guests=self.get_object(pk)
        guests.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  

#3 mixin
#3.1  mixin_list
class Mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Guest.objects.all()
    serializer_class =GuestSerializers

    def get(self,request):
       return self.list(request)
    def post(self,request):
       return self.create(request)

class Mixins_Pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset=Guest.objects.all()
    serializer_class =GuestSerializers

    def get(self,request,pk):
       return self.retrieve(request)
    def put(self,request,pk):
       return self.update(request)
    def delete(self,request,pk):
       return self.destroy(request)
  
#5 Generic
#5.1 get and post
class generics_list(generics.ListCreateAPIView):
    queryset=Guest.objects.all()
    serializer_class =GuestSerializers
    #authentication_classes=[BasicAuthentication]
    authentication_classes=[TokenAuthentication]
    #permission_classes=[IsAuthenticated]

class generics_Pk(generics.RetrieveUpdateDestroyAPIView):
    queryset=Guest.objects.all()
    serializer_class =GuestSerializers
    authentication_classes=[TokenAuthentication]
    #authentication_classes=[BasicAuthentication]
    #permission_classes=[IsAuthenticated]

#6 viewsets
class viewsets_guest(viewsets.ModelViewSet):
    queryset=Guest.objects.all()
    serializer_class =GuestSerializers

class viewsets_movie(viewsets.ModelViewSet):
    queryset=Movie.objects.all()
    serializer_class =MovieSerializers
    filter_backend=[filters.SearchFilter]
    search_fields =['movie']

class viewsets_reservation(viewsets.ModelViewSet):
    queryset=Movie.objects.all()
    serializer_class =ResverationSerializers




@api_view(['GET'])
def find_movie(request):
    movies =Movie.objects.filter(
        hall = request.data['hall'],
        movie = request.data['movie'],)
    serializer =MovieSerializers(movies,many=True)
    return Response(serializer.data)


@api_view(['POST'])
def reservation_movie(request):
    movies = Movie.objects.get(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )
    guest =Guest()
    guest.name =request.data['name']
    guest.mobile =request.data['mobile']
    guest.save()
    reservation =Resveration()
    reservation.guest = guest
    reservation.movie = movies
    reservation.save()
    return Response(status = status.HTTP_201_CREATED) 


class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permissions_classes=[IsAuthorOrReadOnly]
    queryset =Post.objects.all()
    serializer_class = PostSerializers
