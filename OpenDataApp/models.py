from pyexpat import model
from django.db import models
from matplotlib.pyplot import cla

# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=100, blank=True, null=True)
    fulladdress = models.CharField(max_length=1000, blank=True, null=True)
    mappositionX = models.FloatField(blank=True, null=True)
    mappositionY = models.FloatField(blank=True, null=True)  # This field type is a guess.


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

class City(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)

class Contacts(models.Model):
    website = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

class Image(models.Model):
    url = models.CharField(max_length=500, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)

class Organization(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1000, blank=True, null=True)
    inn = models.CharField(max_length=1000, blank=True, null=True)
    type = models.CharField(max_length=1000, blank=True, null=True)
    address = models.ForeignKey(Address, models.DO_NOTHING, blank=True, null=True)
    city = models.ForeignKey(City, models.DO_NOTHING, blank=True, null=True)

class Phones(models.Model):
    value = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    contact = models.ForeignKey(Contacts, models.DO_NOTHING, blank=True, null=True)

class General(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10000, blank=True, null=True)
    description = models.CharField(max_length=1000000, blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    organization = models.ForeignKey(Organization, models.DO_NOTHING, blank=True, null=True)
    contacts = models.ForeignKey(Contacts, models.DO_NOTHING, blank=True, null=True)
    address = models.ForeignKey(Address, models.DO_NOTHING, blank=True, null=True)
    city = models.ForeignKey(City, models.DO_NOTHING, blank=True, null=True)
    image = models.ForeignKey(Image, models.DO_NOTHING, blank=True, null=True)
    
class Gallery(models.Model):
    url = models.CharField(max_length=1000, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    general = models.ForeignKey(General, models.DO_NOTHING, blank=True, null=True)





