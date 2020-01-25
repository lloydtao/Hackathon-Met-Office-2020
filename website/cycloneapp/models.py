from django.db import models

class Cyclone(models.Model):
    sid = models.CharField(max_length=60)
    long = models.FloatField()
    lat = models.FloatField()
    intensity = models.IntegerField()