from django.db import models
from datetime import datetime
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.
class test(models.Model):
    testing_text = models.CharField(max_length = 150)
    testing_date = models.DateTimeField(default = now)

    def __str__(self):
        return self.testing_text

class apiCall(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    base_url = models.TextField()
    headersa1 = models.TextField()
    headersb1 = models.TextField()
    headersa2 = models.TextField()
    headersb2 = models.TextField()
    headersa3 = models.TextField()
    headersb3 = models.TextField()
    httpMethod = models.CharField(max_length=25)

    def __str__(self):
        return self.name