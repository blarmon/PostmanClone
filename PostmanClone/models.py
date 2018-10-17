from django.db import models
from datetime import datetime
from django.utils.timezone import now

# Create your models here.
class test(models.Model):
    testing_text = models.CharField(max_length = 150)
    testing_date = models.DateTimeField(default = now)

    def __str__(self):
        return self.testing_text