
from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('registrar-profesional/',views.profesional, name="Profesional"),
    path('listar-profesional/', views.buscarProfesional, name="listarProfesional"),
    path('modificar-profesional/<pk>/', views.modificarProfesional, name="modificar-profesional"),
    path('eliminar-profesional/<pk>/', views.eliminarProfesional, name="eliminar-profesional"),
    path('registrar-cliente/', views.registrarCliente, name="registrar-cliente"),
    path('listar-cliente/', views.listarCliente, name="listar-cliente"),
    path('modificar-cliente/<pk>/', views.modificarCliente, name="modificar-cliente"),
    path('eliminar-cliente/<pk>/', views.eliminarCliente, name="eliminar-cliente"),
    path('login/', views.login_view.as_view(template_name='web/login.html'), name="login"),
    path('home-profesional/', views.home_profesional, name="homeprofesional"),
    path('home-cliente/', views.home_cliente, name="homecliente"),
    path('home-admin/', views.home_admin, name="homeadmin"),
    path('home-registros/', views.home_registros, name="home-registro"),
    path('home-contrato/', views.home_contrato, name="home-contrato"),
    path('registro-contrato/', views.registro_contrato, name="registro-contrato"),
    path('registro-servicios/', views.registro_servicios, name="registro-servicios"),
    path('contratos-morosos/', views.listar_contratosM, name="contratos-morosos"),
    path('modificar-contrato/', views.modificar_contraro, name="modificar-contrato"),
    path('listar-contrato/', views.listarContrato, name="listar-contrato"),
    #path('detalle-Contrato/<pk>/', views.detalleContrato, name="detalle-Contrato"),
    path('detalles-contrato/<pk>/', views.detalleContrato, name="detalles-contrato"),
    path('asignar-profesional/',views.Asignar_Profesional, name="asignar-profesional"),
    path('home-calendar/',views.home_calendar, name="home-calendar"),
    path('crear-checklist/',views.checkList1, name="checklist"),
    path('listar-checklist/',views.listar_checklist, name="listar-checklist"),
    path('tachar/<pk>',views.tachar, name="tachar"),
    path('cancelar/<pk>',views.cancelar, name="cancelar"),
    path('detalles-servicio/<pk>/', views.listar_servicio_detalle, name="detalles-servicio"),
    path('logout', views.logout, name ='logout'),
    path('actividad-mejora/', views.ingresarActividadMejora, name="actividad-mejora"),
    path('listar-actividad/', views.listar_actividad, name="listar-actividad"),
    path('modificar-actividad/', views.modificarEstadoActividad, name="modificar-actividad"),
    path('crear-solicitud',views.crear_solicitud, name="crear-solicitud"),
    path('listar-solicitud',views.listar_solicitud, name="listar-solicitud"),
    path('responder-checklist/<pk>', views.responderChecklist, name="responder-checklist"),
    path('ficha-terreno/',views.ficha_terreno, name="ficha-terreno"),
    path('home-solicitud/',views.home_solicitud, name="home-solicitud"),
     path('home-prevencion/',views.home_act_mejora, name="home-prevencion"),


    
  
     



]