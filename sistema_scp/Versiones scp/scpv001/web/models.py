# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.hashers import check_password


class Administrador(models.Model):
    id_admin = models.CharField(primary_key=True, max_length=10)
    nombre_completo = models.CharField(max_length=200)
    email_admin = models.CharField(max_length=255)
    password_admin = models.CharField(max_length=30)
    last_login = models.DateField(blank=True, null=True)

    USERNAME_FIELD = 'email_admin'

    class Meta:
        managed = False
        db_table = 'administrador'


class Asesoria(models.Model):
    nro_asesoria = models.FloatField()
    hora_asesoria = models.DateField()
    tipo_asesoria = models.CharField(max_length=50)
    id_servicio = models.OneToOneField('Servicio', models.DO_NOTHING, db_column='id_servicio', primary_key=True)

    class Meta:
        managed = False
        db_table = 'asesoria'


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
    hora_cap = models.DateField()
    asistentes = models.CharField(max_length=255)
    materiales = models.CharField(max_length=100)
    id_servicio = models.OneToOneField('Servicio', models.DO_NOTHING, db_column='id_servicio', primary_key=True)

    class Meta:
        managed = False
        db_table = 'capacitacion'


class Cliente(models.Model):
    id_cliente = models.CharField(primary_key=True, max_length=10)
    nombre_empresa = models.CharField(max_length=100)
    email_cliente = models.CharField(max_length=255)
    password_cliente = models.CharField(max_length=30)
    id_comuna = models.ForeignKey('Comuna', models.DO_NOTHING, db_column='id_comuna')
    telefono_empresa = models.FloatField()
    direccion = models.CharField(max_length=200)
    servicio_activo = models.BooleanField()
    id_tipo_cliente = models.ForeignKey('TipoCliente', models.DO_NOTHING, db_column='id_tipo_cliente')

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


class Emergencia(models.Model):
    nivel_urgencia = models.CharField(max_length=50)
    id_ticket = models.OneToOneField('Ticket', models.DO_NOTHING, db_column='id_ticket', primary_key=True)
    area = models.CharField(max_length=50)
    especialidad = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'emergencia'


class HistorialProfesional(models.Model):
    id_historial_prof = models.FloatField(primary_key=True)
    fecha = models.DateField()
    registro = models.CharField(max_length=255)
    id_profesional = models.ForeignKey('Profesional', models.DO_NOTHING, db_column='id_profesional')

    class Meta:
        managed = False
        db_table = 'historial_profesional'


class Llamada(models.Model):
    duracion = models.DateField()
    id_ticket = models.OneToOneField('Ticket', models.DO_NOTHING, db_column='id_ticket', primary_key=True)

    class Meta:
        managed = False
        db_table = 'llamada'


class Login(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    is_admin = models.BooleanField(default=False, null=True)
    is_prof = models.BooleanField(default=False, null=True)
    is_cliente = models.BooleanField(default=False, null=True)
    id_admin = models.ForeignKey('administrador', models.DO_NOTHING, db_column='id_admin', blank=True, null=True)
    id_prof = models.ForeignKey('Profesional', models.DO_NOTHING, db_column='id_prof', blank=True, null=True)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente', blank=True, null=True)
    last_login = models.DateField(blank=True, null=True)

    USERNAME_FIELD = 'email'

    def check_password(self, raw_password):
        if self.password == raw_password:
            return True
        else:
            return False

    def is_active(self): # line 37
        return True
    
    def is_superuser(self):
        return self.is_admin
        

    class Meta:
        managed = False
        db_table = 'login'


class MultasCliente(models.Model):
    id_multa = models.FloatField(primary_key=True)
    fecha = models.DateField()
    motivo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')

    class Meta:
        managed = False
        db_table = 'multas_cliente'


class PagosCliente(models.Model):
    id_pago = models.FloatField(primary_key=True)
    fecha = models.DateField()
    pago = models.FloatField()
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')

    class Meta:
        managed = False
        db_table = 'pagos_cliente'


class Profesional(models.Model):
    id_profesional = models.CharField(primary_key=True, max_length=10)
    nombre_completo = models.CharField(max_length=200)
    email_prof = models.CharField(max_length=255)
    password_prof = models.CharField(max_length=30)
    id_comuna = models.ForeignKey(Comuna, models.DO_NOTHING, db_column='id_comuna')
    direccion = models.CharField(max_length=200)
    telefono_prof = models.FloatField()
    estado = models.CharField(max_length=100)
    contrato_activo = models.BooleanField()
    id_tipo_profesional = models.ForeignKey('TipoProfesional', models.DO_NOTHING, db_column='id_tipo_profesional')
    last_login = models.DateField(blank=True, null=True)

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


class Servicio(models.Model):
    id_servicio = models.FloatField(primary_key=True)
    fecha_servicio = models.DateField()
    precio = models.FloatField()
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')
    id_profesional = models.ForeignKey(Profesional, models.DO_NOTHING, db_column='id_profesional')

    class Meta:
        managed = False
        db_table = 'servicio'


class ServiciosExtraCliente(models.Model):
    id_servicios_extra = models.FloatField(primary_key=True)
    fecha_solicitud = models.DateField()
    visitas_extra = models.FloatField()
    llamados_extra = models.FloatField()
    capacitacion_extra = models.FloatField()
    modif_lista_chequeo = models.FloatField()
    actualizacion_docs = models.FloatField()
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')

    class Meta:
        managed = False
        db_table = 'servicios_extra_cliente'


class Ticket(models.Model):
    id_ticket = models.FloatField(primary_key=True)
    fecha = models.DateField()
    motivo = models.CharField(max_length=100)
    id_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='id_cliente')
    id_profesional = models.ForeignKey(Profesional, models.DO_NOTHING, db_column='id_profesional')

    class Meta:
        managed = False
        db_table = 'ticket'


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


class VisitaMensual(models.Model):
    nro_visita = models.FloatField()
    motivo = models.CharField(max_length=125)
    lista_chequeo = models.BinaryField(blank=True, null=True)
    nro_modif_lista_chequeo = models.FloatField()
    ficha_prevencion = models.BinaryField(blank=True, null=True)
    id_servicio = models.OneToOneField(Servicio, models.DO_NOTHING, db_column='id_servicio', primary_key=True)

    class Meta:
        managed = False
        db_table = 'visita_mensual'
