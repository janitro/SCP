from django.shortcuts import render, redirect
from django.db import connection 
import cx_Oracle
from web.models import Profesional, Comuna, Cliente, Login, Administrador
from django.contrib.auth import login, authenticate
from django.views.generic.edit import FormView
from .forms import loginForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
import django.contrib.sessions as session
from django.contrib.auth.decorators import login_required

#Login
class login_view(TemplateView):
    def get(self, *args, **kwargs):
        form=loginForm()
        return render(self.request, 'web/login.html',{'form':form})
    
    def post(self,request, *args,**kwargs):
        form = loginForm(self.request.POST)
        if form.is_valid():
            user= authenticate(email=form.cleaned_data['email'],password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(self.request, user)
                    filtro = Login.objects.get(email=form.cleaned_data['email'])
                    if filtro.is_admin:
                        return redirect('homeadmin')
                    elif filtro.is_prof:
                        return redirect('homeprofesional')
                    elif filtro.is_cliente:
                        return redirect('homecliente')
                    else:
                        print("no hay mano")
                else:
                    print("cae aca")
                    return render(self.request, 'web/login.html',{'error_mesagge':'Invalido', 'form':form})
            return render(self.request, 'web/login.html')


# Create your views here.
def home(request):
    return render(request, 'web/001home.html', {})

#Función que llama las comunas 
def SP_listarComunas():
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_COMUNA", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

#Crear función que llama el procedimiento de listar creado en la BD
#Se crea una lista para almacenar el cursor que se recorre con un for y se retorna
def listado_tipo_profesional():
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_TIPO_PROFESIONAL", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

#Crear función que llama la función del procedimiento para registrar un profesional
#Guarda en un objeto llamado data la función que llama el procedimiento de listar los tipos de profesionales
#Llama la solicitud de tipo POST para extraer los nombres de los inputs en el html y darlos como parametros en la función registarProfesional1

def profesional(request):
    data = {
    'tipo_profesional':listado_tipo_profesional(),
    'lista_comuna':SP_listarComunas()
    }
    if request.method == 'POST':
        ID_PROFESIONAL = request.POST.get('id')
        NOMBRE_COMPLETO = request.POST.get('nombre')
        EMAIL_PROF = request.POST.get('email')
        PASSWORD_PROF = request.POST.get('password')
        ID_COMUNA = request.POST.get('lista_comuna')
        DIRECCION = request.POST.get('direccion')
        TELEFONO_PROF = request.POST.get('telefono')
        ESTADO= request.POST.get('estado')
        ID_TIPO_PROFESIONAL = request.POST.get('tipoprof')
        CONTRATO_ACTIVO = request.POST.get('contrato')
        salida= PS_registrarProfesional1(ID_PROFESIONAL,NOMBRE_COMPLETO, EMAIL_PROF, PASSWORD_PROF, ID_COMUNA, DIRECCION, TELEFONO_PROF, ESTADO, ID_TIPO_PROFESIONAL, CONTRATO_ACTIVO)
        if salida == 1:
            data['mensaje'] = 'Agregado correctamente'
        else:
            data['mensaje'] = 'Error al agregar'

    return render(request, 'web/registrar-profesional.html',data)

#Función para llamar el procedimiento de agregar profesional, el cual recibe como parametro las variables de arriba
def PS_registrarProfesional1(ID_PROFESIONAL,NOMBRE_COMPLETO, EMAIL_PROF, PASSWORD_PROF, ID_COMUNA, DIRECCION, TELEFONO_PROF, ESTADO, ID_TIPO_PROFESIONAL, CONTRATO_ACTIVO):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_PROFESIONAL',[ID_PROFESIONAL,NOMBRE_COMPLETO, EMAIL_PROF, PASSWORD_PROF, ID_COMUNA, DIRECCION, TELEFONO_PROF, ESTADO, ID_TIPO_PROFESIONAL, CONTRATO_ACTIVO,salida])
    return salida.getvalue()


#Llamada a la función del procedimiento para otorgarle el rut del html "listarProfesional"
def buscarProfesional(request):
    prof = ""
    if request.method == 'GET':
        ID_PROFESIONAL = request.GET.get('rut')
        salida = PS_buscarProfesional(ID_PROFESIONAL)
        prof = PS_listarProfesional()
    return render(request, 'web/listar-profesional.html', {'salida': salida,'prof':prof})

#Función para llamar el procedimiento de buscar a los profesionales por rut
#Funciona pero no se actualiza en la tabla de "listar-profesional.html"
def PS_buscarProfesional(ID_PROFESIONAL):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('SP_LISTAR_PROFESIONAL_RUT',[ID_PROFESIONAL, salida])
  
    return salida.getvalue()

#Procedimiento que lista todos los profesionales en la tabla de "listar-profesional.html"
def PS_listarProfesional():
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PROFESIONAL_JOIN", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

#Función para modificar profesional
def modificarProfesional(request,pk):
    profesionall = Profesional.objects.get(id_profesional=pk)
    data = {
    'tipo_profesional':listado_tipo_profesional(),
    'lista_comuna':SP_listarComunas(),
    'idp': profesionall.id_profesional,
    'nom': profesionall.nombre_completo,
    'email': profesionall.email_prof,
    'pass': profesionall.password_prof,
    'comid': profesionall.id_comuna.id_comuna,
    'com': profesionall.id_comuna.comuna,
    'direccion': profesionall.direccion,
    'telefono': profesionall.telefono_prof,
    'estado': profesionall.estado,
    'tipoid': profesionall.id_tipo_profesional.id_tipo_profesional,
    'tipo': profesionall.id_tipo_profesional.area_trabajo_profesional,
    'contrat': profesionall.contrato_activo
    }

    if request.method == 'POST':
        ID_PROFESIONAL = request.POST.get('id')
        NOMBRE_COMPLETO = request.POST.get('nombre')
        EMAIL_PROF = request.POST.get('email')
        PASSWORD_PROF = request.POST.get('password')
        ID_COMUNA = request.POST.get('lista_comuna')
        DIRECCION = request.POST.get('direccion')
        TELEFONO_PROF = request.POST.get('telefono')
        ESTADO= request.POST.get('estado')
        ID_TIPO_PROFESIONAL = request.POST.get('tipoprof')
        CONTRATO_ACTIVO = request.POST.get('contrat')
        if CONTRATO_ACTIVO == True:
            CONTRATO_ACTIVO = 1
        else:
            CONTRATO_ACTIVO = 0
        salida= PS_modificarProfesional(ID_PROFESIONAL,NOMBRE_COMPLETO, EMAIL_PROF, PASSWORD_PROF, ID_COMUNA, DIRECCION, TELEFONO_PROF, ESTADO, ID_TIPO_PROFESIONAL, CONTRATO_ACTIVO)
        print(ID_PROFESIONAL,NOMBRE_COMPLETO, EMAIL_PROF, PASSWORD_PROF, ID_COMUNA, DIRECCION, TELEFONO_PROF, ESTADO, CONTRATO_ACTIVO, ID_TIPO_PROFESIONAL)
        if salida == 1:
            data['mensaje'] = 'Modificado correctamente'
            return redirect('listarProfesional')
        else:
            data['mensaje'] = 'Error al modificar'
    return render(request, 'web/modificar-profesional.html',data)

#función que llama el procedimiento para modificar profesional
def PS_modificarProfesional(ID_PROFESIONAL,NOMBRE_COMPLETO, EMAIL_PROF, PASSWORD_PROF, ID_COMUNA, DIRECCION, TELEFONO_PROF, ESTADO, ID_TIPO_PROFESIONAL, CONTRATO_ACTIVO):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_ACTUALIZAR_PROFESIONAL',[ID_PROFESIONAL,NOMBRE_COMPLETO, EMAIL_PROF, PASSWORD_PROF, ID_COMUNA, DIRECCION, TELEFONO_PROF, ESTADO, ID_TIPO_PROFESIONAL, CONTRATO_ACTIVO,salida])
    return salida.getvalue()

#Función para eliminar un profesional
def eliminarProfesional(request,pk):
    profesionall = Profesional.objects.get(id_profesional=pk)
    idpro = profesionall.id_profesional
    salida = PS_eliminarProfesional(idpro)
    return redirect(to="listarProfesional")

#función que llama al procedimiento de eliminar
def PS_eliminarProfesional(ID_PROFESIONAL):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    pr = cursor.callproc('SP_ELIMINAR_PROFESIONAL',[ID_PROFESIONAL, salida])
  
    return salida.getvalue()

def sp_listado_tipo_cliente():
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_TIPO_CLIENTE", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

####################################################################################
#Función para registrar cliente
def registrarCliente(request):
    data = {
    'tipo_cliente':sp_listado_tipo_cliente(),
    'lista_comuna':SP_listarComunas()
    }
    if request.method == 'POST':
        ID_CLIENTE = request.POST.get('id')
        NOMBRE_EMPRESA = request.POST.get('nombre')
        EMAIL_CLIENTE = request.POST.get('email')
        PASSWORD_CLIENTE = request.POST.get('password')
        ID_COMUNA = request.POST.get('lista_comuna')
        TELEFONO_EMPRESA = request.POST.get('telefono')
        DIRECCION = request.POST.get('direccion')
        SERVICIO_ACTIVO= request.POST.get('servicio')
        ID_TIPO_CLIENTE = request.POST.get('tipo')
        salida= PS_registrarCliente(ID_CLIENTE, NOMBRE_EMPRESA, EMAIL_CLIENTE, PASSWORD_CLIENTE, ID_COMUNA, TELEFONO_EMPRESA, DIRECCION, SERVICIO_ACTIVO, ID_TIPO_CLIENTE)
        if salida == 1:
            data['mensaje'] = 'Agregado correctamente'
        else:
            data['mensaje'] = 'Error al agregar'

    return render(request, 'web/registrar-cliente.html',data)

#Función para llamar el procedimiento de registrar un cliente
def PS_registrarCliente(ID_CLIENTE, NOMBRE_EMPRESA, EMAIL_CLIENTE, PASSWORD_CLIENTE, ID_COMUNA, TELEFONO_EMPRESA, DIRECCION, SERVICIO_ACTIVO, ID_TIPO_CLIENTE):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_CLIENTE',[ID_CLIENTE, NOMBRE_EMPRESA, EMAIL_CLIENTE, PASSWORD_CLIENTE, ID_COMUNA, TELEFONO_EMPRESA, DIRECCION, SERVICIO_ACTIVO, ID_TIPO_CLIENTE,salida])
    return salida.getvalue()

#Función para listar los clientes
def listarCliente(request):
    clien = ""
    if request.method == 'GET':
        ID_CLIENTE = request.GET.get('rut')
        clien = PS_listarCliente()
    return render(request, 'web/listar-cliente.html',{'clien':clien})


#Procedimiento que lista todos los clientes en la tabla de "listar-cleinte.html"
def PS_listarCliente():
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_CLIENTE_JOIN", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def modificarCliente(request,pk):
    cliente = Cliente.objects.get(id_cliente=pk)
    data = {
    'tipo_cliente':sp_listado_tipo_cliente(),
    'lista_comuna':SP_listarComunas(),
    'idc': cliente.id_cliente,
    'nom': cliente.nombre_empresa,
    'email': cliente.email_cliente,
    'pass': cliente.password_cliente,
    'comid': cliente.id_comuna.id_comuna,
    'com': cliente.id_comuna.comuna,
    'direccion': cliente.direccion,
    'telefono': cliente.telefono_empresa,
    'estado': cliente.servicio_activo,
    'tipoid': cliente.id_tipo_cliente.id_tipo_cliente,
    'tipo': cliente.id_tipo_cliente.tipo_cliente,
    }
    if request.method == 'POST':
        ID_CLIENTE = request.POST.get('id')
        NOMBRE_EMPRESA = request.POST.get('nombre')
        EMAIL_CLIENTE = request.POST.get('email')
        PASSWORD_CLIENTE = request.POST.get('password')
        ID_COMUNA = request.POST.get('lista_comuna')
        DIRECCION = request.POST.get('direccion')
        TELEFONO_EMPRESA = request.POST.get('telefono')
        SERVICIO_ACTIVO= request.POST.get('servicio')
        ID_TIPO_CLIENTE = request.POST.get('tipocli')
        if SERVICIO_ACTIVO == True:
            SERVICIO_ACTIVO = 1
        else:
            SERVICIO_ACTIVO = 0
        salida= PS_modificarCliente(ID_CLIENTE, NOMBRE_EMPRESA, EMAIL_CLIENTE, PASSWORD_CLIENTE, ID_COMUNA, TELEFONO_EMPRESA, DIRECCION, SERVICIO_ACTIVO, ID_TIPO_CLIENTE)
        print(ID_CLIENTE, NOMBRE_EMPRESA, EMAIL_CLIENTE, PASSWORD_CLIENTE, ID_COMUNA, TELEFONO_EMPRESA, DIRECCION, SERVICIO_ACTIVO, ID_TIPO_CLIENTE)
        if salida == 1:
            data['mensaje'] = 'Modificado correctamente'
            return redirect('listar-cliente')
        else:
            data['mensaje'] = 'Error al modificar'
    return render(request, 'web/modificar-cliente.html',data)

#función que llama el procedimiento para modificar profesional
def PS_modificarCliente(ID_CLIENTE, NOMBRE_EMPRESA, EMAIL_CLIENTE, PASSWORD_CLIENTE, ID_COMUNA, TELEFONO_EMPRESA, DIRECCION, SERVICIO_ACTIVO, ID_TIPO_CLIENTE):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_ACTUALIZAR_CLIENTE',[ID_CLIENTE, NOMBRE_EMPRESA, EMAIL_CLIENTE, PASSWORD_CLIENTE, ID_COMUNA, TELEFONO_EMPRESA, DIRECCION, SERVICIO_ACTIVO, ID_TIPO_CLIENTE,salida])
    return salida.getvalue()

#Función para eliminar un cliente
def eliminarCliente(request,pk):
    cliente = Cliente.objects.get(id_cliente=pk)
    idcliente = cliente.id_cliente
    salida = PS_eliminarCliente(idcliente)
    return redirect(to="listar-cliente")

#función que llama al procedimiento de eliminar
def PS_eliminarCliente(ID_CLIENTE):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    pr = cursor.callproc('SP_ELIMINAR_CLIENTE',[ID_CLIENTE, salida])
  
    return salida.getvalue()


def home_profesional(request):
    return render(request, 'web/004homeprofesional.html', {})


def home_cliente(request):
    return render(request, 'web/012homecliente.html', {})

def home_admin(request):
    return render(request, 'web/021homeadmin.html', {})

def home_registros(request):
    return render(request, 'web/home-registros.html', {})