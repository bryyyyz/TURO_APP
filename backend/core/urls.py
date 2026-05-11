"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as static_serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('turo_api.urls')),
]

# In production (DEBUG=False), Django does not serve MEDIA_URL by default.
# For this project we serve uploaded media directly from the app to ensure
# tutor avatars/listing photos remain accessible after deployment.
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT}),
]

# Keep the dev helper as well (no-op-ish in prod, but fine locally).
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
