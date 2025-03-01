from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
import random
import string


class Voter(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    dob = models.DateField()
    sex = models.CharField(max_length=10)
    address = models.TextField(max_length=255, blank=True)  
    id_type = models.CharField(max_length=50)
    id_number = models.CharField(max_length=50)
    id_doc = models.FileField(upload_to="documents/", null=True, blank=True)
    photo = models.ImageField(upload_to="images/", null=True, blank=True)
    unique_id = models.CharField(max_length=8, unique=True, blank=True)  # Generated ID
    #password = models.CharField(max_length=128)  # Store hashed password
    consent = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=2))
            numbers = ''.join(random.choices(string.digits, k=6))
            unique_id = letters + numbers
            if not Voter.objects.filter(unique_id=unique_id).exists():
                return unique_id

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)  # To verify password correctly

    def __str__(self):
        return self.full_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username