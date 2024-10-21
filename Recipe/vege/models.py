from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class recipes_table(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=200)
    image = models.ImageField(upload_to="recipe")