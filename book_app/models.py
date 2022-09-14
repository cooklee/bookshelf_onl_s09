from django.db import models

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)


class Publisher(models.Model):
    name = models.CharField(max_length=65)
    year = models.IntegerField()