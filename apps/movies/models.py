from django.db import models
from django.utils.timezone import now




class Director(models.Model):
    name = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='directors/', null=True)
    imdb_profile = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def age(self):
        if self.date_of_birth:
            today = now().date()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return "N/A"



class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class Movie(models.Model):
    name = models.CharField(max_length=200)
    year = models.DateField()
    language = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='movies/', null=True, blank=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name