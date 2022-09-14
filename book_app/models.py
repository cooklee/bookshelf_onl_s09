from django.db import models

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    #book_set

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Publisher(models.Model):
    name = models.CharField(max_length=65)
    year = models.IntegerField()


class Genre(models.Model):
    name = models.CharField(max_length=30)

class Book(models.Model):
    title = models.CharField(max_length=64)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)


