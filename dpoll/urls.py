from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from myprojectdpoll.views import home  # Import the homepage view

urlpatterns = [
    path('admin/', admin.site.urls),
    # Root URL for homepage
    path('', home, name='home'),

    # Include app-specific URLs under the 'api/' namespace
    path('api/', include('myprojectdpoll.urls')),

    # Password Reset URLs (Django's built-in views)
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
