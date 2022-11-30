from django.db import models
from django.contrib.auth.models import AbstractUser
import CorporationApp.models as co_model

# Create your models here.

class wards(models.Model):

    wardno = models.CharField(max_length = 200, primary_key=True)
    wardname = models.CharField(max_length = 200)


class houseowner(AbstractUser):
    username  =None
    
    firstname = models.CharField(max_length = 200)
    lastname = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200, unique=True)
    phoneno = models.CharField(max_length = 200, unique=True)
    address = models.CharField(max_length = 1000)
    pincode = models.CharField(max_length = 50)
    wardno = models.ForeignKey(wards, on_delete=models.CASCADE)
    password = models.CharField(max_length = 200)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class slotbooking(models.Model):

    waste_id = models.ForeignKey(co_model.wastes,on_delete=models.CASCADE)
    houseowner_id = models.ForeignKey(houseowner,on_delete=models.CASCADE)
    collection_date = models.DateField(null=False)
    booking_date = models.DateField(null=False)

class bookingstatus(models.Model):

    slot_id = models.ForeignKey(slotbooking, on_delete=models.CASCADE)
    wastecollector_id = models.IntegerField(default= 100)
    status = models.CharField(max_length=200, default="waiting for collection")
    collected_date = models.DateField(null=False)

