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
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm
from .helpers import send_forget_password_mail
from django.contrib.auth import authenticate, login, logout

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
        validated_data["unique_id"] = generate_unique_id()  # Generate Unique ID
        validated_data["password"] = make_password(validated_data["password"])  # Hash password
        return super().create(validated_data)
from django.views.decorators.csrf import csrf_protect
# **Register Voter API**
@csrf_protect
def register_voter(request):
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
            id_doc = files.get("idDoc")
            photo = files.get("photo")
            consent = data.get("consent", "false").lower() == "true"


            if not (full_name and email and phone and dob and sex and address and id_type and id_number):
                return JsonResponse({"error": "All fields are required"}, status=400)

            # Phone validation
            if len(phone) != 10 or not phone.isdigit():
                return JsonResponse({"error": "Phone number must be 10 digits"}, status=400)

            # Age validation
           
            if not address:
               return JsonResponse({"error": "Address is required"}, status=400)
            # Convert dob string to date object
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            if dob.year > 2006:
                return JsonResponse({"error": "You must be at least 18 years old"}, status=400)
            # ID Validation
            if id_type not in ["Aadhar Card", "Voter Id"]:
                return JsonResponse({"error": "Identification type must be 'Aadhar Card' or 'Voter Id'"}, status=400)

            if id_type == "Aadhar Card" and not (len(id_number) == 12 and id_number.isdigit()):
                return JsonResponse({"error": "Aadhar Card must have 12 digits"}, status=400)

            if id_type == "Voter Id" and not re.match(r"^[A-Z]{3}[0-9]{7}$", id_number):
                return JsonResponse({"error": "Voter ID must start with 3 uppercase letters followed by 7 digits"}, status=400)

            if not consent:
                return JsonResponse({"error": "You must consent to the terms"}, status=400)

            # File validation
            if id_doc:
                if not id_doc.name.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                    return JsonResponse({"error": "ID Document must be in PDF, JPG, JPEG, or PNG format"}, status=400)
                if id_doc.size > 5 * 1024 * 1024:  # 5MB limit
                    return JsonResponse({"error": "ID Document must be less than 5MB"}, status=400)

            if photo:
                if not photo.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    return JsonResponse({"error": "Photo must be in JPG, JPEG, or PNG format"}, status=400)
                if photo.size > 2 * 1024 * 1024:  # 2MB limit
                    return JsonResponse({"error": "Photo must be less than 2MB"}, status=400)

            voter = Voter.objects.create(
                full_name=full_name,
                email=email,
                phone=phone,
                dob=dob,
                sex=sex,
                address=address,
                id_type=id_type,
                id_number=id_number,
                id_doc=id_doc,
                photo=photo,
                unique_id=generate_unique_id(),
                consent=consent
            )

            voter.save()

            return JsonResponse({"message": "Voter registered successfully", "UniqueId": voter.unique_id}, status=201)

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@api_view(["POST"])
def login_voter(request):
    unique_id = request.data.get("unique_id")
    password = request.data.get("password")

    if not unique_id or not password:
        return Response({"error": "Unique ID and password are required"}, status=400)

    try:
        voter = Voter.objects.get(unique_id=unique_id)
        if voter.check_password(password):
            return Response({"message": "Login successful!"}, status=200)
        else:
            return Response({"error": "Invalid password"}, status=400)
    except Voter.DoesNotExist:
        return Response({"error": "Invalid Unique ID"}, status=400)

def Logout(request):
    logout(request)
    return redirect('/')

def ChangePassword(request, token):
    context = {}
    
    try:
        profile_obj = Profile.objects.filter(forget_password_token=token).first()
        if not profile_obj:
            messages.error(request, 'Invalid or expired token.')
            return redirect('/forgot/')

        voter_obj = profile_obj.user
        context = {'unique_id': voter_obj.unique_id}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            
            if new_password != confirm_password:
                messages.error(request, 'Both passwords should be equal.')
                return redirect(f'/change-password/{token}/')

            voter_obj.password = make_password(new_password)
            voter_obj.save()

            messages.success(request, 'Password changed successfully. Please login.')
            return redirect('/login/')
        
    except Exception as e:
        print(e)
    
    return render(request, 'changepass.html', context)

def ForgetPassword(request):
    try:
        if request.method == 'POST':
            unique_id = request.POST.get('unique_id')
            
            if not Voter.objects.filter(unique_id=unique_id).first():
                messages.success(request, 'No user found with this Unique ID.')
                return redirect('/forgot/')

            voter_obj = Voter.objects.get(unique_id=unique_id)
            token = str(uuid.uuid4())

            profile_obj, created = Profile.objects.get_or_create(user=voter_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()

            send_forget_password_mail(voter_obj.email, token)
            messages.success(request, 'An email is sent.')
            return redirect('/forgot/')
                
    except Exception as e:
        print(e)
    return render(request, 'forgot.html')



def login_voter_view(request):
    return render(request, 'login.html')
@csrf_protect
def register_view(request):
    return render(request, 'register.html')

def dashboard_view(request):
    return render(request, 'dashboard.html')
# **Page Views**
def home(request):
    return render(request, 'home.html')