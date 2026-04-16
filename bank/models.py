from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Bank(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    swift_code = models.CharField(max_length=100)
    institution_number = models.CharField(max_length=20)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Branch(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name="branches")
    name = models.CharField(max_length=100)
    transit_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.EmailField(default="admin@enigmatix.io")
    capacity = models.PositiveIntegerField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

