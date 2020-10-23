
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registrar-profesional/',views.profesional, name="Profesional"),
    path('listar-profesional/', views.buscarProfesional, name="listarProfesional"),
    path('modificar-profesional/<pk>/', views.modificarProfesional, name="modificar-profesional"),
    path('eliminar-profesional/<pk>/', views.eliminarProfesional, name="eliminar-profesional"),
    path('home-profesional/', views.home_profesional, name="homeprofesional"),
    path('login/', views.login, name="login"),
    path('home-cliente/', views.home_cliente, name="homecliente"),
    path('home-admin/', views.home_admin, name="homeadmin"),
]