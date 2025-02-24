"""
URL configuration for dpoll project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#from django.contrib import admin
#from django.urls import path, include

#urlpatterns = [
 #   path('admin/', admin.site.urls),
  #  path('mymyprojectdpoll/', include('myprojectdpoll.urls')),
#]

from django.contrib import admin
from django.urls import path, include
from myprojectdpoll.views import index  # Import a view for the homepage
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("myprojectdpoll.urls")), 
    #path('mymyprojectdpoll/', include('myprojectdpoll.urls')),  # Ensure this is correctly configured
    path('', index, name='home'),  # Add this line for the root URL
    path('admin/', admin.site.urls),
    path('', include('myprojectdpoll.urls')),  # Include URLs from the voting app
]
if settings.DEBUG:  # Serve static files only in development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])


