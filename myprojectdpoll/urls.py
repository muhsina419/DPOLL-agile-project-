from django.contrib import admin
from django.urls import path, include
from myprojectdpoll import views
from .views import set_password, ChangePassword, Logout, dashboard_view, home,  register_view, ForgetPassword, otp,  upload_id_document, upload_photo
from django.conf import settings
from django.conf.urls.static import static
from .views import upload_photo, upload_id_document,set_password,setpassword,login_voter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login_voter/', views.login_voter, name='login_voter'),
    path('register/', register_view, name='register'),
    path('register-voter/', views.register_view, name='register_voter'),
    path('forgot/', ForgetPassword, name='forgot'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('changepassword/<token>/', ChangePassword, name='changepassword'),
    path('logout/', Logout, name='logout'),
    path('otp/', otp, name='otp'),
    path('register/setpassword/', set_password, name='set_password'),  # API endpoint (POST only)
    path('setpassword/', setpassword, name='setpassword_page'),  
   

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # **URL Patterns**
