from django.shortcuts import render
from django.http.response import JsonResponse
from django.http import Http404

from .models import Guest, Movie, Reservation
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
from rest_framework.generics import GenericAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
# Create your views here.
# 1 no rest no model


def norest_nomodel(request):
    guests = [
        {
            'name': 'mo',
            'movie': 'movie 1'
        }, {
            'name': 'mohamed',
            'movie': 'movie 2'
        }
    ]
    return JsonResponse(guests, safe=False)

# 2 with model ,without rest


def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        'guest': list(data.values('name'))

    }
    return JsonResponse(response)

#create -- post
#read   -- get
#update -- put
#delete -- delete
# pk query -- get

######################

# 3 Function based views
# 3.1 GET POST


@api_view(['GET', 'POST'])
def FBV_list(request):
    # GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    # POST
    elif request.method == "POST":
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GuestSerializer(guest, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 4 Class based views  CBV
# 4.1 Get , Post
class List_CBV(APIView):
    def get(self, request):
        guest = Guest.objects.all()
        serializer = GuestSerializer(guest, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                            serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(
            serializer.data,
            status=status.HTTP_400_BAD_REQUEST)


# 4.2 Get , Put , Delete

class CVB_pk(APIView):
    
    def get_object(self,pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404    
        
    def get(self, request, pk):
        guest=self.get_object(pk)
        serializer=GuestSerializer(guest)
        return Response(serializer.data)

    def put(self, request, pk):
        guest=self.get_object(pk)
        serializer=GuestSerializer(guest,data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest=self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 5 Mixins 
# 5.1 mixins get , post    
class mixins_list(ListModelMixin,CreateModelMixin,GenericAPIView):
    queryset= Guest.objects.all()
    serializer_class=GuestSerializer
    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)

# 5.2 mixins get , put , delete
class mixins_pk(RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,GenericAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    def get(self,request,pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)

    def delete(self, request, pk):
        return self.destroy(request)
    
# 6 generics
# 6.1 get , post

class generics_list(ListCreateAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer   
    
# 6.2 get , put , delete

class generics_pk(RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class=GuestSerializer
    
# 7  viewsets
class viewsets_guest(ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class viewsets_movie(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
 
    
class viewsets_reservation(ModelViewSet):
    queryset=Reservation.objects.all()
    serializer_class= ReservationSerializer
    
    
# find movie using postman
@api_view(['GET'])
def find_movie(request):
    print(request.data["movie_name"])
    movies=Movie.objects.filter(
      
        hall=request.data['hall'],
        movie_name=request.data['movie_name'],
    )    
    serializer=MovieSerializer(movies,many=True)
    return Response(serializer.data)

# New Reservation
@api_view(['POST'])
def new_reservation(request):
    movie=Movie.objects.get(
        hall=request.data['hall'],
        movie_name=request.data['movie_name'],
        
    ) 
    
    guest=Guest()
    guest.name=request.data['name']
    guest.save()
    
    reservation=Reservation()
    reservation.guest=guest
    reservation.movie=movie
    reservation.save()
    
    return Response(status=status.HTTP_201_CREATED)

    



