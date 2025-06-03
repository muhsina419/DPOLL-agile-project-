from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
import random
import string


class Voter(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=20)
    dob = models.DateField()
    sex = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    id_type = models.CharField(max_length=50)
    id_number = models.CharField(max_length=50)
    id_doc = models.FileField(upload_to="documents/", null=True, blank=True)
    photo = models.ImageField(upload_to="images/", null=True, blank=True)
    unique_id = models.CharField(max_length=8, unique=True)
    consent = models.BooleanField(default=False)
    password = models.CharField(
        max_length=128,
        default=make_password("defaultpassword")  # Default hashed password
    )

    def save(self, *args, **kwargs):
        """Override save method to generate a unique ID if not provided."""
        if not self.unique_id:
            self.unique_id = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        """Generate a unique ID consisting of 2 letters and 6 digits."""
        while True:
            letters = ''.join(random.choices(string.ascii_uppercase, k=2))
            numbers = ''.join(random.choices(string.digits, k=6))
            unique_id = letters + numbers
            if not Voter.objects.filter(unique_id=unique_id).exists():
                return unique_id

    def check_password(self, raw_password):
        """Validate the provided password against the stored hashed password."""
        return check_password(raw_password, self.password)

    def set_password(self, password, confirm_password):
        """Set and hash the password after validation."""
        if password != confirm_password:
            raise ValueError("Passwords do not match")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isalpha() for char in password):
            raise ValueError("Password must contain at least one letter")
        self.password = make_password(password)
        self.save()

    def __str__(self):
        return self.full_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True , blank=True)
    unique_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    profile_photo = models.ImageField(upload_to='images/')
    has_voted = models.BooleanField(default=False)  # New field to track voting status

    def __str__(self):
        return self.name

class SetPassword(models.Model):
    id = models.AutoField(primary_key=True)
    unique_id = models.CharField(max_length=8, unique=True)
    password = models.CharField(max_length=128)

    def set_password(self, password, confirm_password):
        """Set and hash the password after validation."""
        if password != confirm_password:
            raise ValueError("Passwords do not match")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isalpha() for char in password):
            raise ValueError("Password must contain at least one letter")
        self.password = make_password(password)
        self.save()

    def check_password(self, raw_password):
        """Validate the provided password against the stored hashed password."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.unique_id
    
class Candidate(models.Model):
    poll = models.ForeignKey('Poll', on_delete=models.CASCADE,related_name='candidates',null=True, blank=True)
    name = models.CharField(max_length=255)
    representation = models.CharField(max_length=255)
    symbol = models.ImageField(upload_to='symbols/', null=True, blank=True)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    votes= models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    

class Vote(models.Model):
    user = models.ForeignKey(
        Voter,
        on_delete=models.CASCADE,
        default=None,  # Set a default value for existing rows
        null=True,
        blank=True
    )
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Vote by {self.user.unique_id} for {self.candidate.name}"
    
# models.py
from django.db import models

class Poll(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def has_started(self):
        from django.utils import timezone
        return timezone.now() >= self.start_time

    def has_ended(self):
        from django.utils import timezone
        return timezone.now() > self.end_time