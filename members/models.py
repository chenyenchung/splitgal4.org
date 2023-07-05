from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass
    affiliation = models.CharField(
        max_length=1024,
        blank=True,
        default=''
    )
    
    lab = models.CharField(
        max_length=128,
        blank=True,
        default=''
    )

    verified = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return self.username