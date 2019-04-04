from django.db import models

# Create your models here.
class State(models.Model):
    current=models.TextField(max_length=10000)
	
    def __str__(self):
        return self.current
    