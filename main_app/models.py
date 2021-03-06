from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


HABITATS = (
    ('G', 'On the ground'),
    ('T', 'In trees or bushes'),
    ('P', 'Perched on a fence or wire'),
    ('N', 'In a nest'),
    ('F', 'Flying'),
    ('W', 'Wading or swimming'),
    ('E', 'Eating at a feeder')
)


# Create your models here.
class Location(models.Model):
    name = models.CharField('Birding location', max_length=100)
    description = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Birding location: {self.name}"

    def get_absolute_url(self):
        return reverse('locations_detail', kwargs={'location_id': self.id})


class Bird(models.Model):
    name = models.CharField('Common Name', max_length=100)
    scientific_name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    invasive = models.BooleanField('Invasive?', default=False)
    locations = models.ManyToManyField(Location)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('birds_detail', kwargs={'bird_id': self.id})


class Sighting(models.Model):
    date = models.DateField()
    habitat = models.CharField(max_length=1, choices=HABITATS, default=HABITATS[0][0])
    bird = models.ForeignKey(Bird, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_habitat_display()} on {self.date}"


class BirdPhoto(models.Model):
    url = models.CharField(max_length=250)
    bird = models.ForeignKey(Bird, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for bird_id: {self.bird_id} @{self.url}"


class LocationPhoto(models.Model):
    url = models.CharField(max_length=250)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for location_id: {self.location_id} @{self.url}"
