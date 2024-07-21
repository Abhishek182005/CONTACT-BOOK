
from django.db import models

class Book(models.Model):
    SNO = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=1000)
    NUMBERS = models.BigIntegerField()
