from django.db import models

# Create your models here.


class PiPosition(models.Model):
    idx = models.BigIntegerField()
    palindrome = models.CharField()
    digits = models.CharField()
