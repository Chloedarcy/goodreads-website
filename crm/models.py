from django.db import models

# Create your models here.
image = models.ImageField(upload_to='img')


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.title} by {self.author}'