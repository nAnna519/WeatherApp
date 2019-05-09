from django.db import models

# Create your models here.

class City(models.Model):
    name = models.Charfield(max_length=30)