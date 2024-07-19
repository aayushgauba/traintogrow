from django.db import models

class Courses(models.Model):
    Title = models.CharField(max_length=100)
    Description = models.TextField()
    Price = models.IntegerField()
    