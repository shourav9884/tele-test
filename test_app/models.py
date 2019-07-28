from django.db import models

# Create your models here.
class TestDB(models.Model):
    test_field = models.IntegerField()
