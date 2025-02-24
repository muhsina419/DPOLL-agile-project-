import re
import random
import string
import json
import base64
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import serializers, views, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Voter

# **Unique ID Generator**
def generate_unique_id():
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    numbers = ''.join(random.choices(string.digits, k=6))
    return letters + numbers

# **Password Validation**
def validate_password(password):
    return bool(re.fullmatch(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password))

# **Serializer for Voter**
class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = ["full_name", "email", "phone", "dob", "sex", "id_type", "id_number", "password"]

    def create(self, validated_data):
        validated_data["unique_id"] = generate_unique_id()  # Generate Unique ID
        validated_data["password"] = make_password(validated_data["password"])  # Hash password
        return super().create(validated_data)

# **Register Voter API**
@csrf_exempt
def register_voter(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Extract Data
            full_name = data.get("fullName", "").strip()
            email = data.get("email", "").strip()
            phone = data.get("phone", "").strip()
            dob = data.get("dateOfBirth", "").strip()
            sex = data.get("sex", "").strip()
            address = data.get("address", "").strip()
            id_type = data.get("identificationType", "").strip()
            id_number = data.get("identificationNumber", "").strip()
            id_document = data.get("idDocument", "")
            photo = data.get("photo", "")
            password = data.get("password", "").strip()
            consent = data.get("consent", False)

            # **Validations**
            if not (full_name and email and phone and dob and sex and address and id_type and id_number and password):
                return JsonResponse({"error": "All fields are required"}, status=400)

            if len(phone) != 10 or not phone.isdigit():
                return JsonResponse({"error": "Phone number must be 10 digits"}, status=400)

            if int(dob.split("-")[0]) > 2006:
                return JsonResponse({"error": "You must be at least 18 years old"}, status=400)

            if id_type not in ["Aadhar Card", "Voter Id"]:
                return JsonResponse({"error": "Identification type must be 'Aadhar Card' or 'Voter Id'"}, status=400)

            if id_type == "Aadhar Card" and not (len(id_number) == 12 and id_number.isdigit()):
                return JsonResponse({"error": "Aadhar Card must have 12 digits"}, status=400)

            if id_type == "Voter Id" and not (re.match(r"^[A-Z]{3}[0-9]{7}$", id_number)):
                return JsonResponse({"error": "Voter ID must start with 3 uppercase letters followed by 7 digits"}, status=400)

            if not consent:
                return JsonResponse({"error": "You must consent to the terms"}, status=400)

            # Create voter
            voter = Voter.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                date_of_birth=dob,
                sex=sex,
                address=address,
                identification_type=id_type,
                identification_number=id_number,
                password=make_password(password),
                unique_id=generate_unique_id()
            )

            # Decode and Save ID Document
            if id_document:
                id_doc_data = base64.b64decode(id_document.split(",")[1])
                voter.id_document.save(f"{voter.id}_id.png", ContentFile(id_doc_data))

            # Decode and Save Photo
            if photo:
                photo_data = base64.b64decode(photo.split(",")[1])
                voter.photo.save(f"{voter.id}_photo.png", ContentFile(photo_data))

            voter.save()

            return JsonResponse({"message": "Voter registered successfully", "UniqueId": voter.unique_id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

# **Login API**
@api_view(["POST"])
def login_voter(request):
    unique_id = request.data.get("unique_id")
    password = request.data.get("password")

    try:
        voter = Voter.objects.get(unique_id=unique_id)
        if check_password(password, voter.password):
            return Response({"message": "Login successful!"}, status=200)
        else:
            return Response({"error": "Invalid password"}, status=400)
    except Voter.DoesNotExist:
        return Response({"error": "Invalid Unique ID"}, status=400)

# **Page Views**
def index(request):
    return render(request, 'home.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')
