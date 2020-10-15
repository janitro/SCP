
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registrarProfesional/',views.profesional, name="Profesional"),
    path('listarProfesional/', views.listadoProfesional, name="listarProfesional"),
]