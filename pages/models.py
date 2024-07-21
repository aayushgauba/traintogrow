from django.db import models

class Courses(models.Model):
    Title = models.CharField(max_length=100)
    Description = models.TextField()
    Price = models.IntegerField()

class Invoice(models.Model):
    Course_id = models.IntegerField()
    profile_id = models.IntegerField()
    Paid = models.BooleanField()
    Date = models.DateField(auto_now_add=True)

class CourseFile(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='course_files/')
