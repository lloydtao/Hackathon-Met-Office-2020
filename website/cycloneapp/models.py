from django.db import models

class Cyclone(models.Model):
    sid = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=128)
    datetime = models.DateTimeField(null=True)

class CycloneNode(models.Model):
    class Meta:
        unique_together = ("time_index", "cyclone")
    
    cyclone = models.ForeignKey("Cyclone", related_name="nodes", related_query_name="nodes_extended_set", on_delete=models.CASCADE)
    time_index = models.IntegerField()
    long = models.FloatField()
    lat = models.FloatField()
    intensity = models.IntegerField(null=True)