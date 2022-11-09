from platform import platform
from shutil import move
from urllib import response
from django.shortcuts import render
from watchlist.api.serializers import*
from watchlist.models import*
from django.http import JsonResponse
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle, ScopedRateThrottle

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView 
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from django.shortcuts import get_object_or_404 
from rest_framework.permissions import IsAuthenticated
from watchlist.api.permission import IsAdminOrReadOnly,IsReviewUserOrReadOnly
from watchlist.api.pagination import WatchListPagination, WatchListCPagination
from watchlist.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters

# generic class based views
class UserReview(generics.ListAPIView):
    serializer_class=ReviewSerializers
    # throttle_classes=[ReviewListThrottle]

    
    # authentication permiss ion
    # permission_classes = [IsAdminOrReadOnly]
    # def get_queryset(self):
    #     username=self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)

    
    def get_queryset(self):
        username=self.request.query_params.get['username', None]
        return Review.objects.filter(review_user__username=username)



class ReviewCreate(generics.CreateAPIView):
    throttle_classes=[ReviewCreateThrottle]

    
    permission_classes = [IsAdminOrReadOnly]

    serializer_class=ReviewSerializers
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk=self.kwargs.get('pk')
        watchlist = Watchlist.objects.get(pk=pk)
        
        review_user=self.request.user
        review_queryset=Review.objects.filter(watchlist=watchlist, review_user=review_user)
        
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie")
           
        if watchlist.number_rating==0:
            watchlist.avg_rating=serializer.validated_data['rating']
        else:
            watchlist.avg_rating=(watchlist.avg_rating + serializer.validated_data['rating'])/2
       
        watchlist.number_rating=watchlist.number_rating + 1
        watchlist.save()
              
        serializer.save(watchlist=watchlist, review_user=review_user)
   
   
    
class ReviewList(generics.ListAPIView):
    # queryset=Review.objects.all()
    serializer_class=ReviewSerializers
    # throttle_classes=[ReviewListThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
     
    # authentication permiss ion
    permission_classes = [IsAdminOrReadOnly]

    
    def get_queryset(self):
        pk=self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)


class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializers
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes=[ScopedRateThrottle]
    throttle_scope='review_detail'



# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializers

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)



# Modelview viewsets

class StreamPlatformAV(viewsets.ModelViewSet):
    permission_classes=[IsAdminOrReadOnly]

    queryset=StreamPlatform.objects.all()
    serializer_class=StreamPlatformSerializers    
    


# viewsets classes
# class StreamPlatformAV(viewsets.ViewSet):
    
#     def list(self, request):
#         queryset=StreamPlatform.objects.all()
#         serializers=StreamPlatformSerializers(queryset, many=True)
#         return Response(serializers.data)
    
#     def retrieve(self, request, pk=None):
#         queryset=StreamPlatform.objects.all()
#         watchlist=get_object_or_404(queryset, pk=pk)
#         serializers=StreamPlatformSerializers(watchlist)
#         return Response(serializers.data )
    
#     def create(self, request):
#         serializer=StreamPlatformSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
    
         
 
 
 
 
 # class based views   
# class StreamPlatformAV(APIView):
    
#     def get(self, request):
#         platform = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializers(platform, many=True, context={'request': request})
#         return Response(serializer.data)
    
    
#     def post(self, request):
#         serializer = StreamPlatformSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


class WatchList(generics.ListAPIView):
    queryset=Watchlist.objects.all()
    serializer_class=WatchlistSerializers
    # throttle_classes=[ReviewListThrottle] 
    
    #  filter_backends = [filters.OrderingFilter]

    # filter_backends = [filters.SearchFilter]
    # ordering_fields = ['avg_rating']
    pagination_class=WatchListCPagination
     

class WatchListAV(APIView):
    
    permission_classes=[IsAdminOrReadOnly]

    
    def get(self, request):
        movie=Watchlist.objects.all()
        serializer=WatchlistSerializers(movie, many=True)
        return Response(serializer.data)
    
    
    def post(self, request):
        serializer=WatchlistSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
        
class StreamDetailAV(APIView):
    
    permission_classes=[IsReviewUserOrReadOnly]
    # throttle_classes=[UserRateThrottle, AnonRateThrottle]

    
    def get(self, request, pk):
        try:           
            stream=StreamPlatform.objects.get(pk=pk)
        except stream.DoesNotExist:
            return Response({'Error': 'Watchlist not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer=StreamPlatformSerializers(stream)
        return Response(serializer.data)
    
    def put(self, request,pk):
        stream=StreamPlatform.objects.get(pk=pk)

        serializer=StreamPlatformSerializers(stream, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request,pk):
        movie=StreamPlatform.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
class WatchlistDetailAV(APIView):
    
    permission_classes=[IsAdminOrReadOnly]
    
    def get(self, request, pk):
        try:           
            movie=Watchlist.objects.get(pk=pk)
        except movie.DoesNotExist:
            return Response({'Error': 'Watchlist not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer=WatchlistSerializers(movie)
        return Response(serializer.data)
    
    def put(self, request,pk):
        Watchlist=Watchlist.objects.get(pk=pk)

        serializer=WatchlistSerializers(Watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request,pk):
        movie=Watchlist.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
        
        
        
        


# Function based views.

# @api_view(['GET', 'POST'])
# def movielist(request):
    
#     if request.method=='GET':
#         movie=Watchlist.objects.all()
#         serializer=Watchlisterializer(movie, many=True)
#         return Response(serializer.data)
    
#     if request.method=='POST':
#         serializer=Watchlisterializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


# @api_view(['GET', 'PUT' , 'DELETE'])
# def movie_details(request, pk):
#     if request.method=='GET':
#         try:           
#             movie=Watchlist.objects.get(pk=pk)
#         except Watchlist.DoesNotExist:
#             return Response({'Error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer=Watchlisterializer(movie)
#         return Response(serializer.data)
    
#     if request.method=='PUT':
#         movie=Watchlist.objects.get(pk=pk)

#         serializer=Watchlisterializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
             
        
#     if request.method=='DELETE':
#         movie=Watchlist.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

        