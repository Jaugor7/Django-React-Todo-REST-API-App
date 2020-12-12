from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from django.views.generic import View

#RestFramework Response Function to Return Serialized Data
from rest_framework.response import Response
#Api_view decorator so that it knows that its an REST API call.
from rest_framework.decorators import api_view

from .serializers import NoteSerializer
from .models import Note


@login_required(login_url='myOauth:login')
def homePage(request):
    print(request.user)
    return render(request, 'index.html')

#We will allow only a GET Request Here
@api_view(['GET'])
def apiOverview(request):

    api_urls = {
        'List' : '',
        'Detail View': '/note-detail/<str:pk>',
        'Create' : '/task-create/',
        'Update' : '/task-update/<str:pk>',
        'Delete' : 'task-delete/<str:pk>',
    }

    return Response(api_urls)

#We only want to allow a GET Response only.
@api_view(['GET'])
def allNotes(request):
    # print(request.user)
    #Get all the Objects of all Entries into the variable notes.
    notes = Note.objects.all()

    #We Will Use NoteSerializer to Serialize Note Objects as Noteserializer Serializes Note Model
    #And we want to serialize more than one item at a time i.e many= True
    serializer = NoteSerializer(notes, many=True) 

    return Response(serializer.data)

# For Single Instance
@api_view(['GET'])
def singleNote(request, pk):

    #Get all the Objects of all Entries into the variable notes.
    notes = Note.objects.get(id = pk)

    #We Will Use NoteSerializer to Serialize Note Objects as Noteserializer Serializes Note Model
    #And we only want to serialize single item i.e many = False
    serialiazer = NoteSerializer(notes, many=False) 

    return Response(serialiazer.data)

# For CREATING NEW NODE
@api_view(['POST'])
def createNote(request):

    #As it is an API View so we have access to request.data for collecting all the data rather than using 
    # request.POST['name'] for every single data that we are accessing
    serializer = NoteSerializer(data = request.data) 

    #request.data gives us an JSON Object

    #Check if Serializer is Valid
    if serializer.is_valid():
        #Save it to DataBase
        serializer.save()

    return Response(serializer.data)

# For Update Our Item
@api_view(['POST'])
def updateNote(request, pk):

    #Extract that note from your DataBase using primary Key
    note = Note.objects.get(id = pk)

    #Give that Same Note to your Serializer and your New Data also
    serializer = NoteSerializer(instance = note, data = request.data)

    #Check if Serializer is Valid
    if serializer.is_valid():
        #Save it to DataBase
        serializer.save()

    return Response("Note Detail Updated Successfully.")

# For Deleting our Note
@api_view(['DELETE'])
def deleteNote(request, pk):

    #Extract that note from your DataBase using primary Key
    note = Note.objects.get(id = pk)

    note.delete()

    return Response("Note Deleted Successfully.")


