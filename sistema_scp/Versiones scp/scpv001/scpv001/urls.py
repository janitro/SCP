from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import login_required, logout_then_login


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('web.urls')),
    
]