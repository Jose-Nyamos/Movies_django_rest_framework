from dataclasses import fields
from pyexpat import model
from rest_framework import serializers

from watchlist.models import*


class ReviewSerializers(serializers.ModelSerializer):
    # review_user=serializers.StringRelatedField(read_only=)
    
    class Meta:
        model=Review
        fields="__all__"

class WatchlistSerializers(serializers.ModelSerializer):
    
    # reviews=ReviewSerializers(many=True, read_only=True)
    platform=serializers.CharField(source='platform.name')     
    
    class Meta:
        model = Watchlist
        fields = '__all__'
        
        
    # def get_len_name(self, object):
    #     return len(object.name)

    # def validate(self,data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("Title and Description should be different")
    #     else:
    #         return data
        
        
    # def validate_name(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short")
        
    #     else:
    #         return value
  
        
class StreamPlatformSerializers(serializers.ModelSerializer):
    
    watchlist=WatchlistSerializers(
        many=True,
        read_only=True
        )

    class Meta:
        model = StreamPlatform
        fields = '__all__'
        
    
        
        

# def name_length(self, value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short")

# class WatchlistSerializer(serializers.Serializer):
#     id=serializers.IntegerField(read_only=True)
#     name=serializers.CharField(validators=[name_length])
#     description=serializers.CharField()
#     active=serializers.BooleanField()
    
#     def create(self, validated_data):
#         return Watchlists.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name=validated_data.get('name', instance.name)
#         instance.description=validated_data.get('description', instance.description)
#         instance.active=validated_data.get('active', instance.active)
        
#         instance.save()

#         return instance
    
#     def validate(self,data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Title and Description should be different")
#         else:
#             return data
    
    # def validate_name(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short")
        
    #     else:
    #         return value
    
    