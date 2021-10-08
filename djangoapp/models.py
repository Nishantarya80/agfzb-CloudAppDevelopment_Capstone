from django.db import models
from django.core import serializers
from django.utils.timezone import now
import uuid
import json

# Create your models here.

class CarMake(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


class CarModel(models.Model):
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
    id = models.AutoField(primary_key=True)
    carMake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    dealerid = models.IntegerField(default=0)
    SEDAN = 'Sedan'
    SUV ='SUV'
    WAGON = 'WAGON'
    CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON'),
    ]
    Type =models.CharField(max_length=30,choices=CHOICES)
    Year=models.DateField(null=True)
    def __str__(self):
        return "Car Make: " + self.carMake 


# <HINT> Create a plain Python class to hold review data