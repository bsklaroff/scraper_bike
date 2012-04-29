from django.db import models

class Model1(models.Model):
    x = models.CharField(max_length=50, blank=True, null=True)
    def __unicode__(self):
        return self.x

class Model2(models.Model):
    y = models.IntegerField(blank=True, null=True)
    z = models.BooleanField()
    a = models.ForeignKey(Model1)
    b = models.DateTimeField()
    def __unicode__(self):
        return self.a.x

