from django.db import models

class DataItem(models.Model):
    key = models.CharField(max_length=100)
    value = models.TextField()