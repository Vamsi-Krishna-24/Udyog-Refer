from django.db import models

class Name(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=False, blank=False)   
    password = models.CharField(max_length=100)


