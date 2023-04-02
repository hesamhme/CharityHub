from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDER_STATUS = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    address = models.TextField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_STATUS, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

