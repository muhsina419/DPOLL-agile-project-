from django.contrib import admin
from django.urls import path, include
from myprojectdpoll import views
from .views import set_password, ChangePassword, Logout, dashboard_view, home, login_voter_view, register_view, ForgetPassword, otp,  upload_id_document, upload_photo
from django.conf import settings
from django.conf.urls.static import static
from .views import upload_photo, upload_id_document,set_password

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_voter_view, name='login'),
    path('register/', register_view, name='register'),
    path('register-voter/', views.register_view, name='register_voter'),
    path('api/login/', login_voter_view, name='login_voter'),
    path('forgot/', ForgetPassword, name='forgot'),
    path('setpassword/', views.set_password, name='setpassword'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('changepassword/<token>/', ChangePassword, name='changepassword'),
    path('logout/', Logout, name='logout'),
    path('otp/', otp, name='otp'),
    path("voters/upload-photo/<unique_id>/", upload_photo, name="upload_photo"),
    path("voters/upload-id/<unique_id>/", upload_id_document, name="upload_id_document"),
    #path('voters/setpassword/', set_password, name='set_password'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # **URL Patterns**
