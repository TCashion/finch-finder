from django.db import models
from django.urls import reverse

# Create your models here.
class Bird(models.Model):
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    date = models.DateField()
    invasive = models.BooleanField(default=False)


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('birds_detail', kwargs={'cat_id' : self.id})