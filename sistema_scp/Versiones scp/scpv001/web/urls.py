
from django.urls import path, include
from . import views
from web.views import reporteSituacionActualView,reporteVisita,reporteCapacitacion,reporteAsesoriaAccidente,reporteAsesoriaFiscalizacion,reporteSolicitud,home_admin,home_profesional,home_cliente


from rest_framework import routers, serializers, viewsets
from .views import ClienteviewSet, CheckViewSet, ServicioviewSet, SearchCalendar, SearchVisitas, SearchSolcitud


router3 = routers.DefaultRouter()
router3.register('cliente', ClienteviewSet)

router2 = routers.DefaultRouter()
router2.register('checklist', CheckViewSet)



router = routers.DefaultRouter()
router.register('calendar', ServicioviewSet)


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
    path('home-profesional/', home_profesional.as_view(), name="homeprofesional"),
    path('home-cliente/', home_cliente.as_view(), name="homecliente"),
    path('home-admin/', home_admin.as_view(), name="homeadmin"),
    path('home-registros/', views.home_registros, name="home-registro"),
    path('home-contrato/', views.home_contrato, name="home-contrato"),
    path('registro-contrato/', views.registro_contrato, name="registro-contrato"),
    path('registro-servicios/', views.registro_servicios, name="registro-servicios"),
    path('contratos-morosos/', views.listar_contratosM, name="contratos-morosos"),
    path('modificar-contrato/', views.modificar_contraro, name="modificar-contrato"),
    path('listar-contrato/', views.listarContrato, name="listar-contrato"),
    #path('detalle-Contrato/<pk>/', views.detalleContrato, name="detalle-Contrato"),
    path('detalles-contrato/<pk>/', views.detalleContrato, name="detalles-contrato"),
    path('agendar_visita/',views.agendar_visita, name="agendar_visita"),
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
    path('situacion-actual/',views.ingresarSituacionActual, name="situacion-actual"),
    path('listar-actividad-cliente/', views.listar_actividad_cliente, name="listar-actividad-cliente"),
    path('responder-actividad/<pk>', views.responderActividad, name="responder-actividad"),
    path('calendar-detail/', views.admin_calendar, name="calendar-detail"),
    path('detalle-calendario/<pk>/', views.listar_calendario_detalle_prof, name="detalle-calendario"),
    path('editar-checklist/<pk>/', views.editarChecklist, name="editar-checklist"),
    #cambios hasta el 04
    path('ajax/mark_notification_as_readed',views.mark_notification_as_readed,name='AJAXMarkNotificationAsReaded'),
    path('crear-alerta', views.crearAlerta, name="crear-alerta"),
    path('home-profesional/chat-room', views.chat_room, name="chat-room"),
    path('room/<str:room_name>/<str:person_name>', views.room, name='room'),
    path('ingresar-asesoria-accidente/<pk>/', views.crear_asesoria_accidente, name="crear-asesoria-accidente"),
    path('ingresar-asesoria-fiscalizacion/<pk>/', views.crear_asesoria_fiscalizador, name="crear-asesoria-fiscalizacion"),
    path('listar-asesoria-accidente/', views.listarAsesoriaAccidente, name="listar-asesoria-accidente"),
    path('modificar-asesoria-accidente/<pk>/', views.modificarAsesoriaAccidente, name="modificar-asesoria-accidente"),
    path('listar-asesoria-fiscalizacion/', views.listarAsesoriaFiscalizacion, name="listar-asesoria-fiscalizacion"),
    path('modificar-asesoria-fiscalizacion/<pk>/', views.modificarAsesoriaFiscalizacion, name="modificar-asesoria-fiscalizacion"),
    path('ingresar-accidente/', views.ingresar_accidente, name="ingresar-accidente"),
    path('crear-capacitacion/<pk>/', views.crear_capacitacion, name="crear-capacitacion"),
    #cambios realizados hasta 07
    path('reportes-all', views.reportAllclient, name="report-all"),

    path('reporte/situacion/<pk>/', reporteSituacionActualView.as_view(), name='situacion-reporte'),
    path('reportes-situacion/', views.templateReportSituacion, name="cliente-reporte-situacion"),
    path('pdf-situacion/', views.pdfSituacionActual_view, name='pdf-situacion'),
    path('reporte/visitas/<pk>/', reporteVisita.as_view(), name='visitas-reporte'),
    path('reportes-visitas/', views.templateReportVisitas, name="cliente-reporte-visitas"),  
    path('pdf-visitas/', views.pdfVisitas_view, name='pdf-visitas'),
    path('reporte/capacitacion/<pk>/', reporteCapacitacion.as_view(), name='visitas-capacitacion'),
    path('reportes-capacitacion/', views.templateReportCapacitacion, name="cliente-reporte-capacitacion"),
    path('pdf-capacitacion/', views.pdfCapacitacion_view, name='pdf-capacitacion'),
    path('reporte/asesoria/accidente/<pk>/', reporteAsesoriaAccidente.as_view(), name='asesoria-accidente'),
    path('reportes-accidente/', views.templateReportAccidente, name="cliente-reporte-accidente"),
    path('pdf-accidente/', views.pdfAccidente_view, name='pdf-accidente'),
    path('reporte/asesoria/fiscalizacion/<pk>/', reporteAsesoriaFiscalizacion.as_view(), name='asesoria-fiscalizacion'),
    path('reportes-fiscalizacion/', views.templateReportFiscalizacion, name="cliente-reporte-fiscalizacion"),
    path('pdf-fiscalizacion/', views.pdfFiscalizacion_view, name='pdf-fiscalizacion'),
    path('reporte/solicitud/<pk>/', reporteSolicitud.as_view(), name='reporte-solicitud'),
    path('reportes-solicitud/', views.templateReportSolicitud, name="cliente-reporte-solicitud"),
    path('pdf-solicitud/', views.pdfSolicitud_view, name='pdf-solicitud'),

    path('listar-capacitacion/', views.listarCapacitacion, name="listar-capacitacion"),
    path('ingresar-resultado/<pk>', views.registrarResultado, name="ingresar-resultado"),
    path('listar-resultado/', views.listarResultado, name='listar-resultado'),
    #pendiente
    path('modificar-solicitud/<pk>',views.modificarEstadoSolicitud, name="modificar-solicitud"),
    path('modificar-capacitacion/<pk>', views.modificarEstadoCapacitacion, name="modificar-capacitacion"),
    path('listar-solicitud-admin',views.listar_solicitud_admin, name="listar-solicitud-admin"),



    #API REST FRAMEWORK
    path('api/', include(router.urls)),
    path('api/', include(router2.urls)),
    path('api/', include(router3.urls)),
    
    path('api/list', SearchCalendar.as_view(), name="list"),
    path('api/visita', SearchVisitas.as_view(), name="visita"),
    path('api/solicitud', SearchSolcitud.as_view(), name="solicitud"),

    #pagos

    path('pagos/', views.pagos_admin, name="pagos"),

    path('comuna/', views.comuna_por_region, name="comuna_por_region"),

    path('visitas/<pk>/', views.Visitas_para_clientes, name="visitas"),

    path('detalles-servicio-cliente/<pk>/', views.listar_servicio_detalle_cliente, name="detalles-servicio-cliente"),
    path('pagos-cliente/<pk>/', views.pagos_cliente, name="pagos-cliente"),
    path('reportes-all-admin', views.reportAllclientAdmin, name="report-all-admin"),
    path('modificar-solicitud-admin/<pk>', views.modificarEstadoSolicitudAdmin, name="modificar-solicitud-admin"),

    

]