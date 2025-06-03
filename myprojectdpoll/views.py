import re
import random
import string
import json
import uuid
from datetime import datetime, timedelta
import pyotp

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.files.storage import default_storage
from django.core.mail import send_mail

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Voter, Profile, SetPassword, UserProfile
from .models import Candidate  # Ensure this import is correct
from .forms import SetPasswordForm
from .helpers import send_forget_password_mail
from .util import send_otp, generate_otp
from django.http import JsonResponse
from .models import Candidate, Vote
from django.db.models import Sum
from datetime import timedelta, date
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SetPassword, Voter
from datetime import datetime
import json


from .models import SetPassword  # Make sure this import is correct
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

            # **Validations**
            if not all([full_name, email, phone, dob_str, sex, address, id_type, id_number, id_doc, photo]):
                return JsonResponse({"error": "All fields are required"}, status=400)

            if Voter.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already registered"}, status=400)
            if Voter.objects.filter(phone=phone).exists():
                return JsonResponse({"error": "Phone number already registered"}, status=400)

            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            if dob.year > 2006:
                return JsonResponse({"error": "You must be at least 18 years old"}, status=400)

            if id_type == "Aadhar Card" and not (len(id_number) == 12 and id_number.isdigit()):
                return JsonResponse({"error": "Aadhar Card must have 12 digits"}, status=400)
            if id_type == "Voter Id" and not re.match(r"^[A-Z]{3}[0-9]{7}$", id_number):
                return JsonResponse({"error": "Voter ID must start with 3 uppercase letters followed by 7 digits"}, status=400)

            # **Create Voter Record**
            unique_id = generate_unique_id()
            voter = Voter.objects.create(
                full_name=full_name, email=email, phone=phone, dob=dob, sex=sex, address=address,
                id_type=id_type, id_number=id_number, id_doc=id_doc, photo=photo,
                unique_id=unique_id, consent=consent
            )
            voter.save()
            
            # **Create UserProfile Record**
            age = datetime.today().year - dob.year - ((datetime.today().month, datetime.today().day) < (dob.month, dob.day))
            UserProfile.objects.create(
                unique_id=unique_id,
                name=full_name,
                age=age,
                email=email,
                phone_number=phone,
                profile_photo=photo,  # Use the photo field from Voter
                has_voted=False  # Default to False
            )

            return JsonResponse({"message": "Registration successful!", "unique_id": voter.unique_id}, status=201)

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

        return JsonResponse({"error": "Invalid request method"}, status=405)

    return render(request, 'register.html')

def reg_success(request,unique_id):
    unique_id = request.GET.get("unique_id")
    return render(request, 'reg_success.html')

def reg_failure(request):
    return render(request, 'reg_failure.html')
# **OTP Verification & Login**
@csrf_exempt
def otp(request,unique_id):
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
                    return redirect('/api/dashboard/')
                else:
                    error_message = "Invalid OTP"
            else:
                error_message = "OTP has expired"
        else:
            error_message = "OTP not found"

    return render(request, 'otp.html', {'unique_id': unique_id})
from .util import generate_otp, send_otp

@csrf_exempt
def send_otp_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone_number = data.get("phone")

            if not phone_number:
                return JsonResponse({"error": "Phone number is required"}, status=400)

            # Generate OTP
            otp = generate_otp()

            # Save OTP and expiration time in session
            request.session["otp"] = otp
            request.session["otp_valid_until"] = (datetime.now() + timedelta(minutes=5)).isoformat()

            # Send OTP to the phone number
            if send_otp(phone_number, otp):
                return JsonResponse({"message": "OTP sent successfully"}, status=200)
            else:
                return JsonResponse({"error": "Failed to send OTP"}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


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
import logging

logger = logging.getLogger(__name__)

# **Password Validation**
def validate_password(password):
    return bool(re.fullmatch(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password))
@csrf_exempt
def set_password(request, unique_id):
    if request.method == "GET":
        # Show the set password form (for registration or forgot password)
        return render(request, 'setpassword.html', {'unique_id': unique_id})

    if request.method == "POST":
        # Handle both JSON and form data
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
                password = data.get("password")
                confirm_password = data.get("confirm_password", password)  # fallback for registration
            except Exception:
                return JsonResponse({"error": "Invalid JSON data"}, status=400)
        else:
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password", password)  # fallback for registration

        if not password or not confirm_password:
            return JsonResponse({"error": "Both password fields are required."}, status=400)
        if password != confirm_password:
            return JsonResponse({"error": "Passwords do not match."}, status=400)
        if not validate_password(password):
            return JsonResponse({
                "error": "Password must be at least 8 characters long and include uppercase, lowercase, number, and special character."
            }, status=400)

        try:
            # Update or create SetPassword entry
            set_password_entry, created = SetPassword.objects.update_or_create(
                unique_id=unique_id,
                defaults={"password": make_password(password)}
            )

            # Update password in Voter model as well
            try:
                voter = Voter.objects.get(unique_id=unique_id)
                voter.password = make_password(password)
                voter.save()
            except Voter.DoesNotExist:
                return JsonResponse({"error": "Voter not found."}, status=404)

            return JsonResponse({"success": True, "message": "Password successfully updated"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def login_voter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            unique_id = data.get('unique_id')
            password = data.get('password')

            if not unique_id or not password:
                return JsonResponse({'error': 'Please provide both unique ID and password'}, status=400)

            try:
                user = SetPassword.objects.get(unique_id=unique_id)
            except SetPassword.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

            if check_password(password, user.password):
                try:
                    voter = Voter.objects.get(unique_id=unique_id)
                except Voter.DoesNotExist:
                    return JsonResponse({'error': 'Voter details not found'}, status=404)
                
                # Generate and send OTP
                otp = generate_otp()
                request.session["otp"] = str(otp)
                request.session["otp_valid_until"] = (datetime.now() + timedelta(minutes=5)).isoformat()
                send_otp(voter.phone, otp)

                # Store user data in session (optional, for dashboard after OTP)
                request.session['user_data'] = {
                    'unique_id': voter.unique_id,
                    'name': voter.full_name,
                    'age': voter.dob.year,  # or calculate age
                    'email': voter.email,
                    'phone': voter.phone,
                    'photo': voter.photo.url if voter.photo else ''
                }

                # Tell frontend to redirect to OTP page
                return JsonResponse({
                    "id": voter.unique_id,
                    "message": "OTP sent. Please verify.",
                    "redirect_url": f"/api/otp/{voter.unique_id}/"
                })
                # Calculate age
                today = datetime.today().date()
                age = today.year - voter.dob.year - ((today.month, today.day) < (voter.dob.month, voter.dob.day))

                # Store user data in session
                request.session['user_data'] = {
                    'unique_id': voter.unique_id,
                    'name': voter.full_name,
                    'age': age,
                    'email': voter.email,
                    'phone': voter.phone,
                    'photo': voter.photo.url if voter.photo else ''
                }

                return JsonResponse({"id":voter.unique_id,'message': 'Login successful', 'redirect_url': '/api/dashboard/'})
            else:
                print("Password validation failed")
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    elif request.method == 'GET':
        return render(request, 'login.html')

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def dashboard_view(request):
    user_data = request.session.get('user_data')
    if not user_data:
        return redirect('/login/')  # Redirect to login if user data is not in session
    return render(request, 'dashboard.html', {'user': user_data})

from django.http import JsonResponse
from .models import Voter

def voters_list_api(request):
    voters = Voter.objects.all().values('unique_id', 'full_name', 'photo', 'email', 'phone')
    for voter in voters:
        voter['photo'] = request.build_absolute_uri(voter['photo']) if voter['photo'] else None
    return JsonResponse(list(voters), safe=False)

def voters_list_view(request):
    voters = Voter.objects.all()  # Fetch all voters from the database
    return render(request, 'voterslist.html', {'voters': voters})

def Logout(request):
    logout(request)
    return redirect('/')

def profile_view(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

def ChangePassword(request, token):
    return render(request, 'changepass.html')

def get_candidates(request):
    candidates = Candidate.objects.all()
    candidate_list = []

    for candidate in candidates:
        candidate_list.append({
            "name": candidate.name,
            "photo": request.build_absolute_uri(candidate.photo.url) if candidate.photo else None,
            "symbol": request.build_absolute_uri(candidate.symbol.url) if candidate.symbol else None,
            "_id": candidate.id,
        })

    return JsonResponse(candidate_list, safe=False)

def ForgetPassword(request):
    return render(request, 'forgot.html')

def candidates_list_view(request):
    candidates = Candidate.objects.all()  # Fetch all candidates from the database
    return render(request, 'candidates_list.html', {'candidates': candidates})

def cast_vote_view(request):
    # Render the voting page only
    candidates = Candidate.objects.all()
    return render(request, "cast_vote.html", {"candidates": candidates})

def results_view(request):
    candidates = Candidate.objects.all()
    results = [
        {
            "name": candidate.name,
            "votes": candidate.votes,
            "symbol": request.build_absolute_uri(candidate.symbol.url) if candidate.symbol else None,
        }
        for candidate in candidates
    ]
    return render(request, 'results.html', {'results': results})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import re
from .models import Voter

@csrf_exempt
def edit_details_view(request):
    if request.method == "POST":
            try:
                data = json.loads(request.body)

                # Extract data from the request
                unique_id = data.get("unique_id")
                full_name = data.get("fullName", "").strip()
                email = data.get("email", "").strip()
                phone = data.get("phone", "").strip()
                dob_str = data.get("dob", "").strip()
                address = data.get("address", "").strip()

                # Validate required fields
                if not all([unique_id, full_name, email, phone, dob_str, address]):
                    return JsonResponse({"error": "All fields are required"}, status=400)

                # Validate email format
                if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    return JsonResponse({"error": "Invalid email format"}, status=400)

                # Validate phone number (must be 10 digits)
                if not (phone.isdigit() and len(phone) == 10):
                    return JsonResponse({"error": "Phone number must be 10 digits"}, status=400)

                # Validate date of birth and age (must be at least 18 years old)
                try:
                    dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
                    today = datetime.today().date()
                    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                    if age < 18:
                        return JsonResponse({"error": "You must be at least 18 years old"}, status=400)
                except ValueError:
                    return JsonResponse({"error": "Invalid date of birth format. Use YYYY-MM-DD"}, status=400)

                # Fetch the voter record
                try:
                    voter = Voter.objects.get(unique_id=unique_id)
                except Voter.DoesNotExist:
                    return JsonResponse({"error": "Voter not found"}, status=404)

                # Update voter details
                voter.full_name = full_name
                voter.email = email
                voter.phone = phone
                voter.dob = dob
                voter.address = address
                voter.updated_at = datetime.now()  # Save the updated date and time
                voter.save()

                return JsonResponse({"message": "Details updated successfully!"}, status=200)

            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON data"}, status=400)
            except Exception as e:
                return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
            return JsonResponse({"error": "Invalid request method"}, status=405)
    return render(request,'edit_details.html')



def polls_view(request):
    return render(request, 'polls.html')

from django.contrib.auth.decorators import login_required
import logging
logger = logging.getLogger(__name__)
@csrf_exempt
def submit_vote(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_unique_id = data.get("unique_id")
            candidate_id = data.get("candidate_id")

            if not user_unique_id or not candidate_id:
                print("Missing unique_id or candidate_id")
                return render(request, "voting_failure.html", {"error": "Missing unique_id or candidate_id"})

            try:
                user = Voter.objects.get(unique_id=user_unique_id)
            except Voter.DoesNotExist:
                print("User not found")
                return render(request, "voting_failure.html", {"error": "User not found."})

            try:
                candidate = Candidate.objects.get(id=candidate_id)
            except Candidate.DoesNotExist:
                print("Candidate not found")
                return render(request, "voting_failure.html", {"error": "Candidate not found."})

            if Vote.objects.filter(user=user).exists():
                print("Already voted")
                return render(request, "voting_failure.html", {"error": "You have already voted."})

            Vote.objects.create(user=user, candidate=candidate)
            print("Vote created: ", vote )
            candidate.votes += 1
            candidate.save()

            try:
                user_profile = UserProfile.objects.get(unique_id=user_unique_id)
                user_profile.has_voted = True
                user_profile.save()
            except UserProfile.DoesNotExist:
                print("User profile not found")
                return render(request, "voting_failure.html", {"error": "User profile not found."})

            context = {
                "candidate_name": candidate.name,
                "transaction_id": Vote.objects.filter(user=user, candidate=candidate).last().id,
                "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            print("Vote successful")
            return render(request, "voting_success.html", context)
        except json.JSONDecodeError:
            print("Invalid JSON data")
            return render(request, "voting_failure.html", {"error": "Invalid JSON data"})
        except Exception as e:
            print(f"Exception: {e}")
            return render(request, "voting_failure.html", {"error": f"An error occurred: {str(e)}"})
    print("Invalid request method")
    return render(request, "voting_failure.html", {"error": "Invalid request method."})

# @csrf_exempt
# def submit_vote(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             user_unique_id = data.get("unique_id")
#             candidate_id = data.get("candidate_id")

#             if not user_unique_id or not candidate_id:
#                 return render(request, "voting_failure.html", {"error": "Missing unique_id or candidate_id"})

#             # Validate user and candidate
#             try:
#                 user = Voter.objects.get(unique_id=user_unique_id)
#             except Voter.DoesNotExist:
#                 return render(request, "voting_failure.html", {"error": "User not found."})

#             try:
#                 candidate = Candidate.objects.get(id=candidate_id)
#             except Candidate.DoesNotExist:
#                 return render(request, "voting_failure.html", {"error": "Candidate not found."})

#             # Check if the user has already voted
#             if Vote.objects.filter(user=user).exists():
#                 return render(request, "voting_failure.html", {"error": "You have already voted."})

#             # Record the vote
#             Vote.objects.create(user=user, candidate=candidate)
        
#             # Increment the candidate's vote count
#             candidate.votes += 1
#             candidate.save()
            
#             # Update the has_voted field in UserProfile
#             try:
#                 user_profile = UserProfile.objects.get(unique_id=user_unique_id)
#                 user_profile.has_voted = True
#                 user_profile.save()
#             except UserProfile.DoesNotExist:
#                 return render(request, "voting_failure.html", {"error": "User profile not found."})

#             # Prepare context for success page
#             context = {
#                 "candidate_name": candidate.name,
#                 "transaction_id": Vote.objects.filter(user=user, candidate=candidate).last().id,
#                 "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             }
#             return render(request, "voting_success.html", context)
#         except json.JSONDecodeError:
#             return render(request, "voting_failure.html", {"error": "Invalid JSON data"})
#         except Exception as e:
#             return render(request, "voting_failure.html", {"error": f"An error occurred: {str(e)}"})
#     return render(request, "voting_failure.html", {"error": "Invalid request method."})

from django.shortcuts import render

def voting_success(request):
    return render(request, 'voting_success.html')

def get_voting_stats(request):
    candidates = Candidate.objects.all()
    stats = [
        {
            "name": candidate.name,
            "votes": candidate.votes,  # Number of votes for the candidate
        }
        for candidate in candidates
    ]
    total_votes = sum(candidate.votes for candidate in candidates)  # Total votes across all candidates

    # Prepare data for the graph (votes vs. candidates)
    graph_data = {
        "labels": [candidate.name for candidate in candidates],  # Candidate names
        "data": [candidate.votes for candidate in candidates],   # Corresponding votes
    }

    return JsonResponse({
        "totalVotes": total_votes,
        "candidates": stats,
        "graphData": graph_data,  # Data for the graph
    }, safe=False)


def get_user_photo(request):
    unique_id = request.GET.get('unique_id')
    print(f"Received unique id : {unique_id}")
    
    if not unique_id:
        return JsonResponse({"error": "Unique ID is required"}, status=400)

    try:
        user_profile = UserProfile.objects.get(unique_id=unique_id)
        eligible = user_profile.age >= 18
        voting_status="Yes" if user_profile.has_voted else "No"
        context = {
            "photo": user_profile.profile_photo.url if user_profile.profile_photo else None,
            "userData":
                {"unique_id":user_profile.unique_id,
                 "eligibility": eligible ,
                 "voting_status": voting_status
                 }
            
            }
        return JsonResponse(context,status=200)
    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    
from .models import UserProfile
def userprofile(request):
    if request.user.is_authenticated:
        try:
            return {'userprofile': UserProfile.objects.get(user=request.user)}
        except UserProfile.DoesNotExist:
            return {'userprofile': None}
    return {'userprofile': None}


def userprofile(request):
    if request.user.is_authenticated:
        try:
            return {'userprofile': UserProfile.objects.get(user=request.user)}
        except UserProfile.DoesNotExist:
            return {'userprofile': None}
    return {'userprofile': None}
# views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Voter
from .util import generate_otp, send_otp

@csrf_exempt
def send_otp_view(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        phone_number = data.get("phone")
        if not phone_number:
            return JsonResponse({"error": "Phone number is required"}, status=400)
        otp = generate_otp()
        request.session["otp"] = str(otp)
        request.session["otp_valid_until"] = (datetime.now() + timedelta(minutes=5)).isoformat()
        if send_otp(phone_number, otp):
            return JsonResponse({"message": "OTP sent successfully"}, status=200)
        else:
            return JsonResponse({"error": "Failed to send OTP"}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def get_phone_by_unique_id(request):
    unique_id = request.GET.get('unique_id')
    if not unique_id:
        return JsonResponse({'error': 'Unique ID is required'}, status=400)
    try:
        voter = Voter.objects.get(unique_id=unique_id)
        return JsonResponse({'phone': voter.phone})
    except Voter.DoesNotExist:
        return JsonResponse({'error': 'Voter not found'}, status=404)
    
# views.py
@csrf_exempt
def get_phone_by_unique_id(request):
    unique_id = request.GET.get('unique_id')
    if not unique_id:
        return JsonResponse({'error': 'Unique ID is required'}, status=400)
    try:
        voter = Voter.objects.get(unique_id=unique_id)
        return JsonResponse({'phone': voter.phone})
    except Voter.DoesNotExist:
        return JsonResponse({'error': 'Voter not found'}, status=404)
    
@csrf_exempt
def verify_otp_view(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        otp_input = data.get('otp')
        session_otp = request.session.get('otp')
        otp_valid_until = request.session.get('otp_valid_until')
        otp_flow = request.session.get('otp_flow')  # 'registration' or 'login'
        unique_id = request.session.get('user_data', {}).get('unique_id')

        if session_otp and otp_valid_until:
            from datetime import datetime
            valid_until = datetime.fromisoformat(otp_valid_until)
            if valid_until > datetime.now():
                if otp_input == session_otp:
                    del request.session['otp']
                    del request.session['otp_valid_until']
                    if 'otp_flow' in request.session:
                        del request.session['otp_flow']
                    # THIS IS WHERE THE REDIRECT IS SET:
                    if otp_flow == 'registration':
                        return JsonResponse({"message": "OTP Verified Successfully!", "redirect": f"/api/reg_success/?unique_id={unique_id}"})
                    else:  # login flow
                        return JsonResponse({"message": "OTP Verified Successfully!", "redirect": "/api/dashboard/"})
                else:
                    return JsonResponse({"error": "Invalid OTP"}, status=400)
            else:
                return JsonResponse({"error": "OTP has expired"}, status=400)
        else:
            return JsonResponse({"error": "OTP not found"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

from .models import Poll, Candidate, Vote

def poll_results(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    candidates = Candidate.objects.filter(poll=poll)
    results = []
    for candidate in candidates:
        votes = Vote.objects.filter(candidate=candidate).count()
        results.append({'candidate': candidate.name, 'votes': votes})
    return render(request, 'poll_results.html', {'poll': poll, 'results': results})

# views.py
from django.shortcuts import render, get_object_or_404
from .models import Poll, Candidate, Vote

def poll_results(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    candidates = Candidate.objects.filter(poll=poll)
    results = []
    for candidate in candidates:
        vote_count = Vote.objects.filter(candidate=candidate).count()
        results.append({
            'candidate': candidate,
            'votes': vote_count
        })
    return render(request, 'poll_results.html', {'poll': poll, 'results': results})

from django.http import JsonResponse
from .models import Voter  # or UserProfile

def unique_id_view(request):
    return render(request, 'unique_id.html')

def get_unique_id(request):
    phone = request.GET.get('phone')
    if not phone:
        return JsonResponse({'error': 'Phone number required'}, status=400)
    try:
        voter = Voter.objects.get(phone=phone)  # <-- changed from phone_number to phone
        return JsonResponse({'unique_id': voter.unique_id})
    except Voter.DoesNotExist:
        return JsonResponse({'error': 'No user found with this phone number'}, status=404)
