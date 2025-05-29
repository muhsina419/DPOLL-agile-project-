from django.contrib import admin
from django.urls import path
from django.conf import settings  # Import settings
from django.conf.urls.static import static  # Import static
from myprojectdpoll import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_voter, name='login_voter'),
    path('register/', views.register_view, name='register'),
    path('forgot/', views.ForgetPassword, name='forgot'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('changepassword/<token>/', views.ChangePassword, name='changepassword'),
    path('logout/', views.Logout, name='logout'),
    path('otp/<str:unique_id>/', views.otp, name='otp'),
    path('setpassword/<str:unique_id>/', views.set_password, name='set_password'),
    path('voters-list/', views.voters_list_view, name='voters_list'),
    path('candidates-list/', views.candidates_list_view, name='candidates_list'),
    path('cast-vote/', views.cast_vote_view, name='cast_vote'),
    path('results/', views.results_view, name='results'),
    path('edit-details/', views.edit_details_view, name='edit_details'),
    path('profile/', views.profile_view, name='profile'),
    path('api/voters/', views.voters_list_api, name='voters_list_api'),
    path('polls/', views.polls_view, name='polls'),
    path('candidates/', views.get_candidates, name='get_candidates'),  # Added trailing slash
    path('vote-stats/', views.get_voting_stats, name='vote-stats'),
    path('voting-success/', views.voting_success, name='voting_success'),
    path('submit-vote/', views.submit_vote, name='submit_vote'),
    path('get_user_photo/', views.get_user_photo, name='get_user_photo'),
    path('send-otp/', views.send_otp_view, name='send_otp'),
    path('get-phone/', views.get_phone_by_unique_id, name='get_phone_by_unique_id'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('reg_success/<str:unique_id>/', views.reg_success, name='reg_success'),
    path('reg_failure/', views.reg_failure, name='reg_failure'),
    path('admin/poll-results/<int:poll_id>/', views.poll_results, name='poll_results'),
    path('admin/poll-results/<int:poll_id>/', views.poll_results, name='poll_results'),
]

# Add static file handling for development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)