from django.db import models

# Create your models here.

class Document(models.Model):
    fichier = models.FileField(upload_to='documents')
    #fichier = models.FileField(upload_to='documents/%Y/%m/%d')
