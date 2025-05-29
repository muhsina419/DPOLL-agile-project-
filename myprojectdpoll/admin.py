from django.contrib import admin
from .models import Voter
from .models import Profile
from .models import UserProfile
from .models import Candidate
from .models import Vote
# Register your models here.


admin.site.register(Voter)
admin.site.register(Profile)
admin.site.register(UserProfile)
admin.site.register(Candidate)
admin.site.register(Vote)
# admin.py
from django.contrib import admin
from .models import Poll

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'is_active')
    list_filter = ('is_active',)
    actions = ['start_poll', 'end_poll']

    def start_poll(self, request, queryset):
        queryset.update(is_active=True)
    start_poll.short_description = "Start selected polls"

    def end_poll(self, request, queryset):
        queryset.update(is_active=False)
    end_poll.short_description = "End selected polls"


