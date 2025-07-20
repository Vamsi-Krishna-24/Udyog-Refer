from django.test import TestCase
from django.db import models

# Create your tests here.
class Name(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name    