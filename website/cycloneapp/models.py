from django.db import models

class Cyclone(models.Model):
    sid = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=128)

class CycloneNode(models.Model):
    class Meta:
        unique_together = ("time_index", "cyclone")
    
    cyclone = models.ForeignKey("Cyclone", related_name="nodes", on_delete=models.CASCADE)
    time_index = models.IntegerField()
    long = models.FloatField()
    lat = models.FloatField()
    intensity = models.IntegerField(null=True)