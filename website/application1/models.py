from django.db import models
from django.contrib.auth.models import User

class Url(models.Model):
    url = models.CharField(max_length=80)
    name = models.CharField(max_length=80)
    file_location = models.CharField(max_length = 60, null=True, blank=True)
    multiple_match = models.BooleanField()
    def __unicode__(self):
        return self.name + " for " + self.url

class Field(models.Model):
    field_name = models.CharField(max_length = 30)
    field_name_ns = models.CharField(max_length = 30)
    match_text = models.CharField(max_length = 10000)
    match_data = models.CharField(max_length = 800)
    ignore_breaks = models.BooleanField()
    url = models.ForeignKey(Url)
    def __unicode__(self):
        return self.field_name + " for " + unicode(self.url)


class MultipleMatch(models.Model):
    field_name = models.CharField(max_length = 30)
    field_name_ns = models.CharField(max_length = 30)
    match_text = models.CharField(max_length = 10000)
    match_data = models.CharField(max_length = 800)
    url = models.ForeignKey(Url)
    def __unicode__(self):
        return self.field_name + " for " + unicode(self.url)
