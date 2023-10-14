from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model=Tasks
    fields=['id','user','task','tocompleted_date','completed','created']

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model=User
    fields=['id','username','email','password']
    
  def create(self,validated_data):
    password=validated_data.pop('password',None)
    instance= self.Meta.model(**validated_data)
    if password is not None:
      instance.set_password(password)
    instance.save()
    return instance