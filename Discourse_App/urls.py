from django.urls import path, include
from . import views
from django.views.generic import TemplateView

# app_name = 'Discourse_App'

urlpatterns = [
    path('create/', views.createNote,  name="createNote"),
    path('update/<str:pk>', views.updateNote,  name="UpdateNote"),
    path('delete/<str:pk>', views.deleteNote,  name="deleteNote"),
    path('note/all/', views.allNotes,  name="allNotes"),
    path('note/<str:pk>/', views.singleNote,  name="singleNote"),
    path('api/', views.apiOverview, name="overview"),
    path('', views.homePage, name="index"),
]
