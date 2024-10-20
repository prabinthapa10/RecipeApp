from django.db import models

# Create your models here.

class recipes_table(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=200)
    image = models.ImageField(upload_to="recipe")