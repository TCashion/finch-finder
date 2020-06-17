from django.db import models
from django.urls import reverse


HABITATS = (
    ('G', 'On the ground'),
    ('T', 'In trees or bushes'),
    ('P', 'Perched on a fence or wire'),
    ('N', 'In a nest'),
    ('F', 'Flying'),
    ('W', 'Wading or swimming'),
)


# Create your models here.
class Bird(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    # date = models.DateField()
    invasive = models.BooleanField(default=False)


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('birds_detail', kwargs={'bird_id' : self.id})


class Sighting(models.Model):
    date = models.DateField()
    habitat = models.CharField(
        max_length = 1,
        choices = HABITATS, 
        default = HABITATS[0][0],
    )
    bird = models.ForeignKey(Bird, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_habitat_display()} on {self.date}"