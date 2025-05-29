from .models import UserProfile

def userprofile(request):
    if request.user.is_authenticated:
        try:
            return {'userprofile': UserProfile.objects.get(user=request.user)}
        except UserProfile.DoesNotExist:
            return {'userprofile': None}
    return {'userprofile': None}