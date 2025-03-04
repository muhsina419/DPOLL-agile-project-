import re
import random
import string
import json
import uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Voter, Profile
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm
from .helpers import send_forget_password_mail
from django.contrib.auth import authenticate, login, logout
from .util import send_otp
from datetime import datetime, timedelta
import pyotp
from django.core.files.storage import default_storage


# **Unique ID Generator**
def generate_unique_id():
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    numbers = ''.join(random.choices(string.digits, k=6))
    return letters + numbers


# **Password Validation**
def validate_password(password):
    return bool(re.fullmatch(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password))


@csrf_exempt
def set_password(request):
    if request.method == "POST":
        unique_id = request.POST.get("unique_id")
        password = request.POST.get("password")

        try:
            voter = Voter.objects.get(unique_id=unique_id)
            voter.password = make_password(password)
            voter.save()
            return JsonResponse({"message": "Password set successfully"}, status=200)
        except Voter.DoesNotExist:
            return JsonResponse({"error": "Invalid Unique ID"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


# **Serializer for Voter**
class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ["full_name", "email", "phone", "dob", "sex", "id_type", "id_number", "id_doc", "photo", "password"]

    def create(self, validated_data):
        validated_data["unique_id"] = generate_unique_id()
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


# **Register Voter API**
@csrf_exempt
def register_view(request):
    if request.method == "POST":
        try:
            data = request.POST
            files = request.FILES

            full_name = data.get("fullName", "").strip()
            email = data.get("email", "").strip()
            phone = data.get("phone", "").strip()
            dob_str = data.get("dateOfBirth", "").strip()
            sex = data.get("sex", "").strip()
            address = data.get("address", "").strip()
            id_type = data.get("identificationType", "").strip()
            id_number = data.get("identificationNumber", "").strip()
            id_doc = files.get("id_doc")
            photo = files.get("photo")
            consent = data.get("consent", "false").lower() == "true"

            if not (full_name and email and phone and dob_str and sex and address and id_type and id_number):
                return JsonResponse({"error": "All fields are required"}, status=400)

            # Uniqueness check
            if Voter.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already registered"}, status=400)
            if Voter.objects.filter(phone=phone).exists():
                return JsonResponse({"error": "Phone number already registered"}, status=400)

            # Age validation
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            if dob.year > 2006:
                return JsonResponse({"error": "You must be at least 18 years old"}, status=400)

            # ID Validation
            if id_type == "Aadhar Card" and not (len(id_number) == 12 and id_number.isdigit()):
                return JsonResponse({"error": "Aadhar Card must have 12 digits"}, status=400)
            if id_type == "Voter Id" and not re.match(r"^[A-Z]{3}[0-9]{7}$", id_number):
                return JsonResponse({"error": "Voter ID must start with 3 uppercase letters followed by 7 digits"}, status=400)

            voter = Voter.objects.create(
                full_name=full_name, email=email, phone=phone, dob=dob, sex=sex, address=address,
                id_type=id_type, id_number=id_number, id_doc=id_doc, photo=photo,
                unique_id=generate_unique_id(), consent=consent
            )
            voter.save()

            return JsonResponse({"message": "Voter registered successfully", "UniqueId": voter.unique_id}, status=201)

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return render(request, 'register.html')


# **OTP Verification & Login**
@csrf_exempt
def otp(request):
    error_message = None
    if request.method == "POST":
        otp = request.POST['otp']
        unique_id = request.session.get('unique_id')

        otp_secret_key = request.session.get('otp_secret_key')
        otp_valid_until = request.session.get('otp_valid_until')

        if otp_secret_key and otp_valid_until:
            valid_until = datetime.fromisoformat(otp_valid_until)
            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    user = get_object_or_404(Voter, unique_id=unique_id)
                    login(request, user)
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_until']
                    return redirect('/dashboard/')
                else:
                    error_message = "Invalid OTP"
            else:
                error_message = "OTP has expired"
        else:
            error_message = "OTP not found"

    return render(request, 'otp.html', {'error_message': error_message})


def Logout(request):
    logout(request)
    return redirect('/')


def ChangePassword(request, token):
    return render(request, 'changepass.html')


def ForgetPassword(request):
    return render(request, 'forgot.html')


def login_voter_view(request):
    return render(request, 'login.html')


def dashboard_view(request):
    return render(request, 'dashboard.html')


def home(request):
    return render(request, 'home.html')


# **Upload Photo**
@csrf_exempt
def upload_photo(request, unique_id):
    if request.method == 'POST' and request.FILES.get('photo'):
        photo = request.FILES['photo']
        file_path = default_storage.save(f'images/{unique_id}_{photo.name}', photo)
        file_url = request.build_absolute_uri(settings.MEDIA_URL + file_path)
        return JsonResponse({'file_url': file_url}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)


# **Upload ID Document**
@csrf_exempt
def upload_id_document(request, unique_id):
    if request.method == "POST" and request.FILES.get("id_doc"):
        id_doc = request.FILES["id_doc"]
        file_path = default_storage.save(f'documents/{unique_id}_{id_doc.name}', id_doc)
        file_url = request.build_absolute_uri(settings.MEDIA_URL + file_path)
        return JsonResponse({"message": "ID document uploaded successfully", "file_url": file_url})
    return JsonResponse({"error": "Invalid request"}, status=400)
