from django.db import models
from django.conf import settings
from django.utils import timezone

class Note(models.Model):
    note = models.CharField(max_length = 100)
        
    def __str__(self):
        return self.note
    