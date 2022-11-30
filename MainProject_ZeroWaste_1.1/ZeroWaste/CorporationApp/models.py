from django.db import models

# Create your models here.
class wastes(models.Model):

    waste_type = models.CharField(max_length = 200, null = False)
    charge = models.FloatField(max_length = None,null = False)