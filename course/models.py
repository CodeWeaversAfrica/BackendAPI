from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=255)
    # Add more fields as needed

    def __str__(self):
        return self.name
