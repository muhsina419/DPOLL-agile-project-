from django.contrib import admin
from django.urls import path, include
from myprojectdpoll import views
from .views import register_voter, set_password, ChangePassword, Logout, dashboard_view, home, login_voter_view, register_view, ForgetPassword
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', home, name='home'),
    path('login/', login_voter_view, name='login'),
    path('register/',views.register_view, name='register'),
    path("api/register-voter/",register_voter, name='register_voter'),
    path("api/login/", views.login_voter_view),  # Ensure this path is correct
    path("forgot/", ForgetPassword, name="forgot"),
    path("setpassword/", set_password, name="password"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("changepassword/<token>/", ChangePassword, name="changepassword"),
    path('logout/', Logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)