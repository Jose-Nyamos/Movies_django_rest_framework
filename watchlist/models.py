from email.policy import default
from platform import platform
from pyexpat import model
from wsgiref.validate import validator
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


# Create your models here.

class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=30)
    website = models.URLField(max_length=30)
    
    def __str__(self):
        return self.name
    
    


class Watchlist(models.Model):
    title=models.CharField(max_length=20, null=True, blank=True)
    description=models.CharField(max_length=30, null=True, blank=True)
    platform=models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="watchlist")
    active=models.BooleanField(default=True)
    avg_rating=models.FloatField(default=0)
    number_rating=models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Review(models.Model):
    review_user=models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description=models.CharField(max_length=200, null=True)
    active  = models.BooleanField(default=True)
    watchlist=models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name="reviews")
    created=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.rating) + " | " + self.watchlist.title + " | " + str(self.review_user)
    
    
    

    
