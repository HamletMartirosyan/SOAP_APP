from django.db import models


# Create your models here.
class Exchange(models.Model):
    iso = models.TextField()
    amount = models.TextField()
    rate = models.TextField()
    difference = models.TextField()
    date = models.DateField()

    def __str__(self):
        return f"ISO={self.iso}, Amount={self.amount}, Rate={self.rate}, Difference={self.difference}, Date={self.date}"
