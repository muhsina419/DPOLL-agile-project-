from django.contrib import admin
from .models import Voter
from .models import Profile
from .models import UserProfile
# Register your models here.


admin.site.register(Voter)
admin.site.register(Profile)
admin.site.register(UserProfile)




