from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Note
from django.conf import settings

# class AuthSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username',)

#Note Serializer Will Serialize Note Model
class NoteSerializer(serializers.ModelSerializer):
    # author = AuthSerializer()
    class Meta:
        model = Note

        #Specify All the Field in the form of a list that you want
        #Or Just Specify only like this shown Below
        fields = '__all__'