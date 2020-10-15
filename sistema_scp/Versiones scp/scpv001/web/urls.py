
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registrar-profesional/',views.profesional, name="Profesional"),
    path('listar-profesional/', views.buscarProfesional, name="listarProfesional"),
    path('modificar-profesional/<pk>/', views.modificarProfesional, name="modificar-profesional"),
    path('eliminar-profesional/<pk>/', views.eliminarProfesional, name="eliminar-profesional"),
]