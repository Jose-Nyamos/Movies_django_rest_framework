from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist.api import serializers
from watchlist import models

class StreamPlatformTestCase(APITestCase):
    
    
    def setUp(self):
        self.user=User.objects.create_user(username="admin", password="1234")
        token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        
    
    def test_streamplatform_create(self):
        data={
            "name": "Netflix",
            "about": "#1 Streaming Platform",
            "website": "https://www.netflix.com"
        }
        response=self.client.post(reverse('streamplatform.list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED), 
