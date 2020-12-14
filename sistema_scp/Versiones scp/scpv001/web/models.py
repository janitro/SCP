# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.hashers import check_password
from django.contrib.auth import password_validation

class Accidente(models.Model):
    id_accidente = models.FloatField(primary_key=True)
    id_cliente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='id_cliente', blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    hora = models.CharField(max_length=20, blank=True, null=True)
    lugar_accidente = models.CharField(max_length=200, blank=True, null=True)
    trabajo_habitual = models.BooleanField(blank=True, null=True)
    tiene_experiencia = models.BooleanField(blank=True, null=True)
    tarea_autorizacion = models.BooleanField(blank=True, null=True)
    desc_lesion = models.CharField(max_length=500, blank=True, null=True)
    grado_lesion = models.CharField(max_length=500, blank=True, null=True)
    contingencia = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accidente'


class ActividadMejora(models.Model):
    id_actividad = models.FloatField(primary_key=True)
    id_cliente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='id_cliente', blank=True, null=True)
    origen = models.CharField(max_length=30, blank=True, null=True)
    actividad = models.CharField(max_length=500, blank=True, null=True)
    estado = models.CharField(max_length=30, blank=True, null=True)
    evidencia_texto = models.CharField(max_length=1000, blank=True, null=True)
    evidencia_imagen = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actividad_mejora'


class Administrador(models.Model):
    id_admin = models.CharField(primary_key=True, max_length=10)
    nombre_completo = models.CharField(max_length=200)
    email_admin = models.CharField(unique=True, max_length=255)
    password_admin = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'administrador'


class Alerta(models.Model):
    id_alerta = models.FloatField(primary_key=True)
    asignado_a = models.ForeignKey('Profesional', models.DO_NOTHING, db_column='asignado_a', blank=True, null=True)
    creado_por = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='creado_por', blank=True, null=True)
    titulo = models.CharField(max_length=60, blank=True, null=True)
    descripcion = models.CharField(max_length=1000, blank=True, null=True)
    respondido = models.BooleanField(blank=True, null=True)
    fecha_creacion = models.DateField(blank=True, null=True)
    antigua_instancia = models.ForeignKey('self', models.DO_NOTHING, db_column='antigua_instancia', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'alerta'


class AsesoriaAccidente(models.Model):
    id_servicio = models.OneToOneField('Servicio', models.DO_NOTHING, db_column='id_servicio', primary_key=True)
    id_profesional = models.ForeignKey('Profesional', models.DO_NOTHING, db_column='id_profesional', blank=True, null=True)
    inspeccion_lugar_accidente = models.BooleanField(blank=True, null=True)
    verificar_contrato_accidentado = models.BooleanField(blank=True, null=True)
    planificar_capacitacion_riesgos = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asesoria_accidente'


class AsesoriaFiscalizacion(models.Model):
    id_servicio = models.ForeignKey('Servicio', models.DO_NOTHING, db_column='id_servicio', blank=True, null=True)
    ente_fiscalizador = models.ForeignKey('EnteFiscalizador', models.DO_NOTHING, db_column='ente_fiscalizador', blank=True, null=True)
    fecha_fiscalizacion = models.DateField(blank=True, null=True)
    detalle_evento = models.CharField(max_length=2000, blank=True, null=True)
    juicio = models.BooleanField(blank=True, null=True)
    conversacion_fiscalizador = models.BooleanField(blank=True, null=True)
    evidenciar_documentacion = models.BooleanField(blank=True, null=True)
    contingencia = models.CharField(max_length=2000, blank=True, null=True)
    id_profesional = models.ForeignKey('Profesional', models.DO_NOTHING, db_column='id_profesional', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asesoria_fiscalizacion'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Capacitacion(models.Model):
    asistentes = models.ForeignKey('Profesional', models.DO_NOTHING, db_column='asistentes')
    materiales = models.CharField(max_length=100)
    id_servicio = models.OneToOneField('Servicio', models.DO_NOTHING, db_column='id_servicio', primary_key=True)
    id_tipo_capacitacion = models.ForeignKey('TipoCapacitacion', models.DO_NOTHING, db_column='id_tipo_capacitacion', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'capacitacion'


class Checklist(models.Model):
    id = models.FloatField(primary_key=True)
    checklist = models.CharField(max_length=250, blank=True, null=True)
    resultado = models.BooleanField(blank=True, null=True)
    id_cliente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='id_cliente', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'checklist'


class Cliente(models.Model):
    id_cliente = models.CharField(primary_key=True, max_length=10)
    nombre_empresa = models.CharField(max_length=100)
    email_cliente = models.CharField(unique=True, max_length=255)
    password_cliente = models.CharField(max_length=1000)
    id_comuna = models.ForeignKey('Comuna', models.DO_NOTHING, db_column='id_comuna')
    telefono_empresa = models.FloatField()
    direccion = models.CharField(max_length=200)
    servicio_activo = models.BooleanField()
    id_tipo_cliente = models.ForeignKey('TipoCliente', models.DO_NOTHING, db_column='id_tipo_cliente')
    id_profesional = models.ForeignKey('Profesional', models.DO_NOTHING, db_column='id_profesional')

    class Meta:
        managed = False
        db_table = 'cliente'


class Comuna(models.Model):
    id_comuna = models.FloatField(primary_key=True)
    comuna = models.CharField(max_length=125)
    id_region = models.ForeignKey('Region', models.DO_NOTHING, db_column='id_region')

    class Meta:
        managed = False
        db_table = 'comuna'


class Contrato(models.Model):
    id_contrato = models.FloatField(primary_key=True)
    fecha_contrato = models.DateField()
    detalles_contrato = models.CharField(max_length=255)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')

    class Meta:
        managed = False
        db_table = 'contrato'


class DetalleFactura(models.Model):
    id_detalle_factura = models.IntegerField(primary_key=True)
    id_factura = models.ForeignKey('Factura', models.DO_NOTHING, db_column='id_factura', blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    llamadas_extra = models.IntegerField(blank=True, null=True)
    capacitacion_extra = models.IntegerField(blank=True, null=True)
    asesoria_extra = models.IntegerField(blank=True, null=True)
    modif_lista_chequeo = models.IntegerField(blank=True, null=True)
    actualizacion_docs = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalle_factura'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DocsCliente(models.Model):
    id_docs_cliente = models.FloatField(primary_key=True)
    fecha_emision = models.DateField()
    doc_visita_mensual = models.BinaryField(blank=True, null=True)
    doc_capacitacion = models.BinaryField(blank=True, null=True)
    doc_asesoria = models.BinaryField(blank=True, null=True)
    doc_resumen_mensual = models.BinaryField(blank=True, null=True)
    doc_ficha_prevencion = models.BinaryField(blank=True, null=True)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')

    class Meta:
        managed = False
        db_table = 'docs_cliente'


class EnteFiscalizador(models.Model):
    id_ente_fiscalizador = models.FloatField(primary_key=True)
    ente_fiscalizador = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ente_fiscalizador'


class EstadoServicio(models.Model):
    id_estado_servicio = models.IntegerField(primary_key=True)
    descripcion = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'estado_servicio'


class EstadoSolicitud(models.Model):
    id_estado_solicitud = models.FloatField(primary_key=True)
    estado_solicitud = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estado_solicitud'


class Factura(models.Model):
    id_factura = models.FloatField(primary_key=True)
    fecha = models.DateField()
    tipo_servicio = models.CharField(max_length=25)
    estado_factura = models.CharField(max_length=20)
    factura_neta = models.IntegerField()
    iva = models.IntegerField()
    factura_total = models.IntegerField()
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')

    class Meta:
        managed = False
        db_table = 'factura'


class HistorialProfesional(models.Model):
    id_historial_prof = models.FloatField(primary_key=True)
    fecha = models.DateField()
    registro = models.CharField(max_length=255)
    id_profesional = models.ForeignKey('Profesional', models.DO_NOTHING, db_column='id_profesional')

    class Meta:
        managed = False
        db_table = 'historial_profesional'


class Login(models.Model):
    id_login = models.FloatField(primary_key=True)
    email = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    is_admin = models.BooleanField(blank=True, null=True)
    is_prof = models.BooleanField(blank=True, null=True)
    is_cliente = models.BooleanField(blank=True, null=True)
    id_admin = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='id_admin', blank=True, null=True)
    id_prof = models.ForeignKey('Profesional', models.DO_NOTHING, db_column='id_prof', blank=True, null=True)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente', blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'login'


class MotivoVisita(models.Model):
    id_motivo_visita = models.IntegerField(primary_key=True)
    tipo_visita = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'motivo_visita'


class MultasCliente(models.Model):
    id_multa = models.FloatField(primary_key=True)
    fecha = models.DateField()
    motivo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')

    class Meta:
        managed = False
        db_table = 'multas_cliente'


class Notificacion(models.Model):
    id_notificacion = models.FloatField(primary_key=True)
    asignado_a = models.ForeignKey('Profesional', models.DO_NOTHING, db_column='asignado_a', blank=True, null=True)
    fecha_creacion = models.DateField(blank=True, null=True)
    leido = models.BooleanField(blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    pk_relacion = models.FloatField(blank=True, null=True)
    asignado_a_c = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='asignado_a_c', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notificacion'


class PagosCliente(models.Model):
    id_pago = models.FloatField(primary_key=True)
    fecha = models.DateField()
    pago = models.FloatField()
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')

    class Meta:
        managed = False
        db_table = 'pagos_cliente'


class Precio(models.Model):
    contrato = models.IntegerField()
    llamadas = models.IntegerField()
    capacitacion = models.IntegerField()
    asesoria = models.IntegerField()
    modif_lista_chequeo = models.IntegerField()
    actualizacion_docs = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'precio'


class Profesional(models.Model):
    id_profesional = models.CharField(primary_key=True, max_length=10)
    nombre_completo = models.CharField(max_length=200)
    email_prof = models.CharField(unique=True, max_length=255)
    password_prof = models.CharField(max_length=1000)
    id_comuna = models.ForeignKey(Comuna, models.DO_NOTHING, db_column='id_comuna')
    direccion = models.CharField(max_length=200)
    telefono_prof = models.FloatField()
    estado = models.CharField(max_length=100)
    contrato_activo = models.BooleanField()
    id_tipo_profesional = models.ForeignKey('TipoProfesional', models.DO_NOTHING, db_column='id_tipo_profesional')
    carga_trabajo = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'profesional'


class Region(models.Model):
    id_region = models.FloatField(primary_key=True)
    region = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'region'


class RegistroError(models.Model):
    id_reg_error = models.FloatField(primary_key=True)
    sentencia_error = models.CharField(max_length=70)
    mensaje_error = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'registro_error'


class Resultado(models.Model):
    id_resultado = models.FloatField(primary_key=True)
    id_servicio = models.ForeignKey('Servicio', models.DO_NOTHING, db_column='id_servicio', blank=True, null=True)
    fecha_finalizacion = models.DateField(blank=True, null=True)
    analisis = models.CharField(max_length=2000, blank=True, null=True)
    resultado = models.CharField(max_length=2000, blank=True, null=True)
    areas_oportunidad = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'resultado'


class Servicio(models.Model):
    id_servicio = models.FloatField(primary_key=True)
    fecha_servicio = models.DateField()
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')
    id_estado_servicio = models.ForeignKey(EstadoServicio, models.DO_NOTHING, db_column='id_estado_servicio')
    id_motivo_visita = models.ForeignKey(MotivoVisita, models.DO_NOTHING, db_column='id_motivo_visita')
    hora_servicio = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'servicio'


class ServiciosExtraCliente(models.Model):
    id_servicios_extra = models.FloatField(primary_key=True)
    fecha_solicitud = models.DateField()
    llamados_extra = models.FloatField()
    capacitacion_extra = models.FloatField()
    modif_lista_chequeo = models.FloatField()
    actualizacion_docs = models.FloatField()
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')
    asesorias_extra = models.FloatField()

    class Meta:
        managed = False
        db_table = 'servicios_extra_cliente'


class SituacionActual(models.Model):
    id_situacion = models.FloatField(primary_key=True)
    situacion_actual = models.CharField(max_length=1000, blank=True, null=True)
    propuesta_general = models.CharField(max_length=1000, blank=True, null=True)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'situacion_actual'


class Solicitud(models.Model):
    id_solicitud = models.FloatField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente', blank=True, null=True)
    id_profesional = models.CharField(max_length=10, blank=True, null=True)
    id_tipo_solicitud = models.ForeignKey('TipoSolicitud', models.DO_NOTHING, db_column='id_tipo_solicitud', blank=True, null=True)
    detalle = models.CharField(max_length=500, blank=True, null=True)
    fecha_creacion = models.DateField(blank=True, null=True)
    hora_creacion = models.CharField(max_length=10, blank=True, null=True)
    id_estado_solicitud = models.ForeignKey(EstadoSolicitud, models.DO_NOTHING, db_column='id_estado_solicitud', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'solicitud'


class TipoCapacitacion(models.Model):
    id_tipo_capacitacion = models.FloatField(primary_key=True)
    nombre_capacitacion = models.CharField(max_length=200, blank=True, null=True)
    unidad_tematica = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_capacitacion'


class TipoCliente(models.Model):
    id_tipo_cliente = models.FloatField(primary_key=True)
    tipo_cliente = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tipo_cliente'


class TipoProfesional(models.Model):
    id_tipo_profesional = models.FloatField(primary_key=True)
    area_trabajo_profesional = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tipo_profesional'


class TipoSolicitud(models.Model):
    id_tipo_solicitud = models.FloatField(primary_key=True)
    tipo_solicitud = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tipo_solicitud'

