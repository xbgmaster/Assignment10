from django.db import models

# Create your models here.
class NumberSet(models.Model):
        country = models.TextField()
        capital = models.TextField()
        population = models.TextField()
        temperature_celsius = models.TextField()
        weather_description = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
        return f"Set on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


