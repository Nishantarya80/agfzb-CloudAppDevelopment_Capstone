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
        return "Car name: " + self.name  

class DealerReview:
    def __init__(self,dealership,name,purchase,review,purchase_date,car_make,car_model,car_year,sentiment,id):
        self.dealership=dealership
        self.name=name
        self.purchase=purchase
        self.review=review
        self.purchase_date=purchase_date
        self.car_make=car_make
        self.car_model=car_model
        self.car_year=car_year
        self.sentiment=sentiment
        self.id=id
    def __str__(self):
        return "name: " + self.name


# <HINT> Create a plain Python class to hold review data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name