from django.db import models
import random
import string
from django.contrib.auth.hashers import make_password, check_password

class Voter(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    dob = models.DateField()
    sex = models.CharField(max_length=10)
    id_type = models.CharField(max_length=50)
    id_number = models.CharField(max_length=50)
    id_doc = models.FileField(upload_to="id_docs/", null=True, blank=True)
    photo = models.FileField(upload_to="photos/", null=True, blank=True)
    unique_id = models.CharField(max_length=8, unique=True, blank=True)  # Generated ID
    #password = models.CharField(max_length=128)  # Store hashed password
    password = models.CharField(max_length=128, null=True, blank=True)  # Temporarily allow blank


    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = self.generate_unique_id()
        if not self.password.startswith('pbkdf2_sha256$'):  # Prevent re-hashing an already hashed password
            self.password = make_password(self.password)
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
