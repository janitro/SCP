
from web import models
from web.models import Login
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

#Se crea un backends para la autentificacion del mdoelo "Profesional" ya que este no cuenta con
# una autentificacion ni login por predeterminado.
# Debe ser llamado en settings.py

class LoginBackend(BaseBackend):
    def authenticate(self,request, email=None, password=None):
        try:
            user = Login.objects.get(email=email)
            success = Login.password
            if success:
                return user
        except Login.DoesNotExist:
            pass
        return None

    def get_user(self, id):
        try:
            return Login.objects.get(id=id)
        except Login.DoesNotExist:
            return None