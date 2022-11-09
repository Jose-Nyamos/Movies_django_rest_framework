from django.urls import path, include 
from watchlist.api.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter() 

router.register('stream',StreamPlatformAV, basename='streamplatform')

urlpatterns = [
    
    path('list/', WatchListAV.as_view(), name='movies_list'),
    path('<int:pk>/', WatchlistDetailAV.as_view(), name='movies_detail'),
    path('list2/', WatchList.as_view(), name='watch-list'),

    # path('stream/', StreamPlatformAV.as_view(), name='stream'),
   
    path('', include(router.urls)),
   
    path('<int:pk>/review_create', ReviewCreate.as_view(), name='create_review'),
    path('<int:pk>/reviews', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>', ReviewDetails.as_view(),name="review-detail" ),
    path('reviews/', UserReview.as_view(),name="user-review-detail")

]
