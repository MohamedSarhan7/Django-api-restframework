from django.db import models

# Create your models here.

# guest --- movie -- reservation


class Movie (models.Model):
    movie_name = models.CharField(max_length=50)
    hall = models.CharField(max_length=10)
    # date = models.DateField()

    def __str__(self):
        return self.movie_name


class Guest (models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    guest = models.ForeignKey(
        Guest, on_delete=models.CASCADE, related_name='reservation')
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name='reservation')

    def __str__(self):
        return f"{self.guest.name}-{self.movie.movie_name}"
