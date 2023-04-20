from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class User(AbstractUser):
    pass


class Mobile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    phone_no = PhoneNumberField()

    def __str__(self):
        return f"{self.user} {self.phone_no}"
    

