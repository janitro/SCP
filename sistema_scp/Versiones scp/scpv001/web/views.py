from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection 
import cx_Oracle
from django.utils import datastructures
from web.models import *
from django.contrib.auth import login, authenticate
from django.views.generic.edit import FormView
from web.forms import *
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
import django.contrib.sessions as session
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import logout as do_logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.core import serializers
from django.views.generic import View
import base64
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from xhtml2pdf import pisa
from django.template.loader import get_template
import base64
from django.utils.decorators import method_decorator
from django.db.models import Count, Max, Sum
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from rest_framework import viewsets, generics, status
from .serializers import *
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import filters
from rest_framework import serializers


#Login
class login_view(TemplateView):
    def get(self, *args, **kwargs):
        form=loginForm()
        return render(self.request, 'web/login.html',{'form':form})
    
    def post(self,request, *args,**kwargs):
        form = loginForm(self.request.POST)
        if form.is_valid():
            user= authenticate(request,email=form.cleaned_data['email'],password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active :
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


def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')




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
    'lista_comuna':SP_listarComunas(),
    'lista_region': PS_listarRegion()
    }
    if request.method == 'POST':
        ID_PROFESIONAL = request.POST.get('id')
        NOMBRE_COMPLETO = request.POST.get('nombre')
        EMAIL_PROF = request.POST.get('email')
        PASS = request.POST.get('password')
        send_email(EMAIL_PROF,PASS,NOMBRE_COMPLETO)
        PASSWORD_PROF = make_password(request.POST.get('password'),None,'default')
        ID_COMUNA = request.POST.get('lista_comuna')
        DIRECCION = request.POST.get('direccion')
        TELEFONO_PROF = request.POST.get('telefono')
        ESTADO= request.POST.get('estado')
        ID_TIPO_PROFESIONAL = request.POST.get('tipoprof')
        CONTRATO_ACTIVO = request.POST.get('contrato')
        salida= PS_registrarProfesional1(ID_PROFESIONAL,NOMBRE_COMPLETO, EMAIL_PROF, PASSWORD_PROF, ID_COMUNA, DIRECCION, TELEFONO_PROF, ESTADO, ID_TIPO_PROFESIONAL, CONTRATO_ACTIVO)
        if salida == 1:
            messages.success(request, "Agregado correctamente")
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
    ID_PROFESIONAL = ""
    if request.method == 'POST':
        ID_PROFESIONAL = request.POST.get('rut')
        salida = PS_buscarProfesional(ID_PROFESIONAL)
        if ID_PROFESIONAL == "":
            salida = PS_listarProfesional()
            return render(request,'web/listar-profesional.html',{'salida':salida})
    else:
        salida = PS_listarProfesional()
        return render(request,'web/listar-profesional.html',{'salida':salida})
    return render(request, 'web/listar-profesional.html', {'salida':salida})


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
        
     

        salida= PS_modificarProfesional(ID_PROFESIONAL,NOMBRE_COMPLETO, EMAIL_PROF, PASSWORD_PROF, ID_COMUNA, DIRECCION, TELEFONO_PROF, ESTADO, ID_TIPO_PROFESIONAL, CONTRATO_ACTIVO)
        print(ID_PROFESIONAL,NOMBRE_COMPLETO, EMAIL_PROF, PASSWORD_PROF, ID_COMUNA, DIRECCION, TELEFONO_PROF, ESTADO, CONTRATO_ACTIVO, ID_TIPO_PROFESIONAL)
        if salida == 1:
            messages.success(request, "Modificado correctamente")
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
    'lista_comuna':SP_listarComunas(),
    'lista_profesional':PS_listarProfesional(),
    'lista_region': PS_listarRegion()
    }
    if request.method == 'POST':
        ID_CLIENTE = request.POST.get('id')
        NOMBRE_EMPRESA = request.POST.get('nombre')
        EMAIL_CLIENTE = request.POST.get('email')
        PASS = request.POST.get('password')
        send_email(EMAIL_CLIENTE,PASS,NOMBRE_EMPRESA)
        PASSWORD_CLIENTE = make_password(request.POST.get('password'),None,'default')
        ID_COMUNA = request.POST.get('lista_comuna')
        TELEFONO_EMPRESA = request.POST.get('telefono')
        DIRECCION = request.POST.get('direccion')
        SERVICIO_ACTIVO = request.POST.get('servicio')
        ID_TIPO_CLIENTE = request.POST.get('tipo')
        ID_PROFESIONAL = request.POST.get('lista_profesional')
        salida= PS_registrarCliente(ID_CLIENTE, NOMBRE_EMPRESA, EMAIL_CLIENTE, PASSWORD_CLIENTE, ID_COMUNA, TELEFONO_EMPRESA, DIRECCION, SERVICIO_ACTIVO, ID_TIPO_CLIENTE, ID_PROFESIONAL)
        if salida == 1:
            messages.success(request, "Agregado correctamente")
            data['mensaje'] = 'Agregado correctamente'
        else:
            messages.error(request, "Error al agregar")
            data['mensaje'] = 'Error al agregar'

    return render(request, 'web/registrar-cliente.html',data)

#Función para llamar el procedimiento de registrar un cliente
def PS_registrarCliente(ID_CLIENTE, NOMBRE_EMPRESA, EMAIL_CLIENTE, PASSWORD_CLIENTE, ID_COMUNA, TELEFONO_EMPRESA, DIRECCION, SERVICIO_ACTIVO, ID_TIPO_CLIENTE, ID_PROFESIONAL):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_CLIENTE',[ID_CLIENTE, NOMBRE_EMPRESA, EMAIL_CLIENTE, PASSWORD_CLIENTE, ID_COMUNA, TELEFONO_EMPRESA, DIRECCION, SERVICIO_ACTIVO, ID_TIPO_CLIENTE, ID_PROFESIONAL, salida])
    return salida.getvalue()

#Función para listar los clientes
def listarCliente(request):
    clien = ""
    if request.method == 'POST':
        ID_CLIENTE = request.POST.get('rut')
        salida = PS_buscarCliente(ID_CLIENTE)
        if ID_CLIENTE == "":
            salida = PS_listarCliente()
            return render (request, 'web/listar-cliente.html',{'salida':salida})
    else:
        salida = PS_listarCliente()
        return render (request, 'web/listar-cliente.html',{'salida':salida})
    return render(request, 'web/listar-cliente.html',{'salida':salida})


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
    'lista_profesional':PS_listarProfesional(),
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
    'idprof': cliente.id_profesional.id_profesional,
    'prof': cliente.id_profesional.nombre_completo,
    
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
        ID_PROFESIONAL = request.POST.get('lista_profesional')

      
        salida= PS_modificarCliente(ID_CLIENTE, NOMBRE_EMPRESA, EMAIL_CLIENTE, PASSWORD_CLIENTE, ID_COMUNA, TELEFONO_EMPRESA, DIRECCION, SERVICIO_ACTIVO, ID_TIPO_CLIENTE, ID_PROFESIONAL)
        print(ID_CLIENTE, NOMBRE_EMPRESA, EMAIL_CLIENTE, PASSWORD_CLIENTE, ID_COMUNA, TELEFONO_EMPRESA, DIRECCION, SERVICIO_ACTIVO, ID_TIPO_CLIENTE, ID_PROFESIONAL)
        if salida == 1:
            messages.success(request, "Modificado correctamente")
            data['mensaje'] = 'Modificado correctamente'
            return redirect('listar-cliente')
        else:
            data['mensaje'] = 'Error al modificar'
    return render(request, 'web/modificar-cliente.html',data)

#función que llama el procedimiento para modificar profesional
def PS_modificarCliente(ID_CLIENTE, NOMBRE_EMPRESA, EMAIL_CLIENTE, PASSWORD_CLIENTE, ID_COMUNA, TELEFONO_EMPRESA, DIRECCION, SERVICIO_ACTIVO, ID_TIPO_CLIENTE, ID_PROFESIONAL):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_ACTUALIZAR_CLIENTE',[ID_CLIENTE, NOMBRE_EMPRESA, EMAIL_CLIENTE, PASSWORD_CLIENTE, ID_COMUNA, TELEFONO_EMPRESA, DIRECCION, SERVICIO_ACTIVO, ID_TIPO_CLIENTE, ID_PROFESIONAL,salida])
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

@method_decorator(login_required, name='dispatch')
class home_profesional(TemplateView):
    template_name = 'web/004homeprofesional.html'

    def notificacion(self):
        id_profesional = self.request.user.id_prof.id_profesional
        profesional = Profesional.objects.get(id_profesional=id_profesional)
        notificacions = profesional.notificacion_asignada_a_profesional.order_by('fecha_creacion')
        old_notifications = notificacions.filter(leido=True).order_by('-fecha_creacion')
        old_notifications = old_notifications[:5]
        return old_notifications

    def cantidad_solicitud(self):
        profesional = self.request.user.id_prof.id_profesional
        solicitud = Solicitud.objects.filter(id_profesional=profesional,id_estado_solicitud=1).count()
        return solicitud
    
    def alertas_anuales(self):
        profesional = self.request.user.id_prof.id_profesional
        year = datetime.now().year
        alerta = Alerta.objects.filter(asignado_a=profesional, fecha_creacion__year=year).count()
        return alerta
    
    def cantidad_capacitacion(self):
        profesional = self.request.user.id_prof.id_profesional
        capacitacion = Servicio.objects.filter(id_cliente__id_profesional=profesional,id_motivo_visita=3).count()
        return capacitacion 
    
    def cantidad_asesoria_accidente(self):
        profesional = self.request.user.id_prof.id_profesional
        accidente = Servicio.objects.filter(id_cliente__id_profesional=profesional,id_motivo_visita=4).count()
        return accidente
    
    def cantidad_asesoria_fiscalizacion(self):
        profesional = self.request.user.id_prof.id_profesional
        fiscalizacion = Servicio.objects.filter(id_cliente__id_profesional=profesional,id_motivo_visita=5).count()
        return fiscalizacion

    def get_capacitacion_profesional(self):
        data = []
        try:    
            profesional = self.request.user.id_prof.id_profesional
            print(profesional)
            for e in EstadoServicio.objects.all():
                capacitacion = Servicio.objects.filter(id_estado_servicio=e.id_estado_servicio,id_cliente__id_profesional=profesional,id_motivo_visita=3).count()
                data.append({
                    'name': e.descripcion,
                    'y': capacitacion
                })
        except:
            pass  
        return data
    
    def get_asesoria_accidente(self):
        data = []
        try:    
            profesional = self.request.user.id_prof.id_profesional
            print(profesional)
            for e in EstadoServicio.objects.all():
                accidente = Servicio.objects.filter(id_estado_servicio=e.id_estado_servicio,id_cliente__id_profesional=profesional,id_motivo_visita=4).count()
                data.append({
                    'name': e.descripcion,
                    'y': accidente
                })
        except:
            pass  
        return data
    
    def get_asesoria_fiscalizacion(self):
        data = []
        try:    
            profesional = self.request.user.id_prof.id_profesional
            print(profesional)
            for e in EstadoServicio.objects.all():
                fiscalizacion = Servicio.objects.filter(id_estado_servicio=e.id_estado_servicio,id_cliente__id_profesional=profesional,id_motivo_visita=5).count()
                data.append({
                    'name': e.descripcion,
                    'y': fiscalizacion
                })
        except:
            pass  
        return data
    
    def get_cantidad_accidentes(self):
        data = []
        try:
            year = datetime.now().month
            profesional = self.request.user.id_prof.id_profesional
            for m in range(1, 13):
                accidente = Accidente.objects.filter(id_cliente__id_profesional=profesional,fecha__month=m).count()
                data.append(accidente)
        except:
            pass 
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de profesional'
        context['capacitacion_profesional'] = self.get_capacitacion_profesional()
        context['asesoria_accidente'] = self.get_asesoria_accidente()
        context['asesoria_fiscalizacion'] = self.get_asesoria_fiscalizacion()
        context['cantidad_solicitud'] = self.cantidad_solicitud()
        context['cantidad_alerta'] = self.alertas_anuales()
        context['cantidad_accidentes'] = self.get_cantidad_accidentes()
        context['cantidad_capacitacion'] = self.cantidad_capacitacion()
        context['cantidad_asesoria_accidente'] = self.cantidad_asesoria_accidente()
        context['cantidad_asesoria_fiscalizacion'] = self.cantidad_asesoria_fiscalizacion()
        context['old_notifications'] = self.notificacion

        return context

@method_decorator(login_required, name='dispatch')
class home_cliente(TemplateView):
    template_name = 'web/012homecliente.html'

    def get_asesoria_accidente(self):
        data = []
        try:    
            cliente = self.request.user.id_cliente.id_cliente
            for e in EstadoServicio.objects.all():
                accidente = Servicio.objects.filter(id_estado_servicio=e.id_estado_servicio,id_cliente=cliente,id_motivo_visita=4).count()
                data.append({
                    'name': e.descripcion,
                    'y': accidente
                })
        except:
            pass  
        return data
    
    def get_asesoria_fiscalizacion(self):
        data = []
        try:    
            cliente = self.request.user.id_cliente.id_cliente
            for e in EstadoServicio.objects.all():
                accidente = Servicio.objects.filter(id_estado_servicio=e.id_estado_servicio,id_cliente=cliente,id_motivo_visita=5).count()
                data.append({
                    'name': e.descripcion,
                    'y': accidente
                })
        except:
            pass  
        return data
    
    def get_capacitacion(self):
        data = []
        try:    
            cliente = self.request.user.id_cliente.id_cliente
            for e in EstadoServicio.objects.all():
                accidente = Servicio.objects.filter(id_estado_servicio=e.id_estado_servicio,id_cliente=cliente,id_motivo_visita=3).count()
                data.append({
                    'name': e.descripcion,
                    'y': accidente
                })
        except:
            pass  
        return data
    
    def cantidad_capacitacion(self):
        cliente = self.request.user.id_cliente.id_cliente
        capacitacion = Servicio.objects.filter(id_cliente=cliente,id_motivo_visita=3).count()
        return capacitacion 
    
    def cantidad_asesoria_accidente(self):
        cliente = self.request.user.id_cliente.id_cliente
        accidente = Servicio.objects.filter(id_cliente=cliente,id_motivo_visita=4).count()
        return accidente
    
    def cantidad_asesoria_fiscalizacion(self):
        cliente = self.request.user.id_cliente.id_cliente
        fiscalizacion = Servicio.objects.filter(id_cliente=cliente,id_motivo_visita=5).count()
        return fiscalizacion
    
    def cantidad_actividad(self):
        cliente = self.request.user.id_cliente.id_cliente
        actividad = ActividadMejora.objects.filter(id_cliente=cliente,estado='Pendiente').count()
        return actividad


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de cliente'
        context['asesoria_accidente'] = self.get_asesoria_accidente()
        context['asesoria_fiscalizacion'] = self.get_asesoria_fiscalizacion()
        context['capacitacion'] = self.get_capacitacion()
        context['cantidad_capacitacion'] = self.cantidad_capacitacion()
        context['cantidad_asesoria_accidente'] = self.cantidad_asesoria_accidente()
        context['cantidad_asesoria_fiscalizacion'] = self.cantidad_asesoria_fiscalizacion()
        context['cantidad_actividad'] = self.cantidad_actividad()
        return context


def ficha_terreno(request):
    return render(request, 'web/home-ficha-terreno.html', {})

def home_solicitud(request):
    return render(request, 'web/home-solicitud.html', {})

def home_act_mejora(request):
    return render(request, 'web/home-actividad-mejora.html', {})



@method_decorator(login_required, name='dispatch')
class home_admin(TemplateView):
    template_name = 'web/021homeadmin.html'
    def get_profesional(self):
        data = []
        try:
            for p in Profesional.objects.all():
                profesional = p.nombre_completo
                data.append(profesional)
        except:
            pass  
        return data

    def get_accidente_profesional(self):
        data = []
        try:
            profesional = Profesional.objects.all()
            for c in profesional:
                accidentes = Accidente.objects.filter(id_cliente__id_profesional=c.id_profesional).count()
                if accidentes > 0:
                    data.append(accidentes)
        except:
            pass 
        return data
    
    def get_capacitacion_profesional(self):
        data = []
        try:    
            profesional = Profesional.objects.all()
            for c in profesional:
                capacitacion = Servicio.objects.filter(id_cliente__id_profesional=c.id_profesional,id_motivo_visita=3).count()
                data.append(capacitacion)
        except:
            pass  
        return data

    def get_asesoria_accidente(self):
        data = []
        try:
            estado = EstadoServicio.objects.all()
            for e in estado:
                asesoria = Servicio.objects.filter(id_estado_servicio=e.id_estado_servicio, id_motivo_visita=4).count()
                data.append({
                    'name': e.descripcion,
                    'y': asesoria
                })
        except:
            pass  
        return data
    
    def get_cantidad_accidentes(self):
        data = []
        try:
            year = datetime.now().month
            for m in range(1, 13):
                accidente = Accidente.objects.filter(fecha__month=m).count()
                data.append(accidente)
        except:
            pass 
        return data
    
    def cantidad_capacitacion(self):
        capacitacion = Capacitacion.objects.all().count()
        return capacitacion
    
    def cantidad_asesoria(self):
        accidente =  Servicio.objects.filter(id_motivo_visita=4).count()
        fiscalizacion = Servicio.objects.filter(id_motivo_visita=5).count()
        total = (accidente + fiscalizacion)
        return total
    
    def cantidad_accidente(self):
        accidente = Accidente.objects.all().count()
        return accidente 
    
    def cantidad_solicitud_reporte(self):
        solicitud = Solicitud.objects.filter(id_tipo_solicitud=6,id_estado_solicitud=1).count()
        return solicitud

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['panel'] = 'Panel de administrador'
        context['accidente_profesional'] = self.get_accidente_profesional()
        context['profesional'] = self.get_profesional()
        context['capacitacion_profesional'] = self.get_capacitacion_profesional()
        context['asesoria_accidente'] = self.get_asesoria_accidente()
        context['cantidad_accidente'] = self.get_cantidad_accidentes()
        context['cantidad_capacitacion'] = self.cantidad_capacitacion()
        context['cantidad_asesoria'] = self.cantidad_asesoria()
        context['cantidad_accidente_2'] = self.cantidad_accidente()
        context['cantidad_solicitud'] = self.cantidad_solicitud_reporte()
        return context


def home_registros(request):
    return render(request, 'web/home-registros.html', {})


#Contratos y Servicios

def home_contrato(request):
    return render(request, 'web/home-contrato.html', {})


def registro_contrato(request):
    return render(request, 'web/registro-contrato.html', {})

def registro_servicios(request):
    return render(request, 'web/home-asignar.html', {})


def listar_contratosM(request):
    contra = ""
    if request.method == 'GET':
       ID_CLIENTE = request.GET.get('rut')
       contra = PS_listarContratoMorosos()
        
    return render(request, 'web/listar-contrato-M.html', {'contra':contra})


def PS_listarContratoMorosos():
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_contrato_NONE", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista





def PS_listarContrato():
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_CONTRATO", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


def listarContrato(request):
    contra = ""
    if request.method == 'GET':
        ID_CLIENTE = request.GET.get('rut')
        
        contra = PS_listarContrato()
        
        
    return render(request, 'web/listar-contrato.html',{'contra':contra})


def detalleContrato(request,pk):
    cliente = Cliente.objects.get(id_cliente=pk)
    idcliente = cliente.id_cliente
    data = PS_buscarContrato(idcliente)
    
    

    return render(request, 'web/detalles-contrato.html', {'data':data})






def PS_buscarContrato(ID_CLIENTE):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('sp_listar_contrato_detail',[ID_CLIENTE, salida])
  
    return salida.getvalue()
 
    



def modificar_contraro(request):
    return render(request, 'web/modificar-contrato.html', {})


def listado_motivo_visita():
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_motivo_visita", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista



def listado_estado_servicio():
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_ESTADO_SERVICIO", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista



def listado_cliente_prof(id_profesional):
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_cliente_rut_prof", [out_cur, id_profesional])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


def agendar_visita(request, date=None):
    id_profesional = request.user.id_prof.id_profesional
    data = {
        'listar_motivo':listado_motivo_visita(),
        'listar_cliente':PS_listar_cliente(id_profesional),
        'estado_servicio':listado_estado_servicio(),
    } 
    if request.method == 'POST':

        FECHA_SERVICIO = request.POST.get('fecha')
        ID_CLIENTE = request.POST.get('listar_cliente')
        ID_ESTADO_SERVICIO = request.POST.get('estado_servicio')
        id_motivo_visita = request.POST.get('listar_motivo')
        hora_servicio = request.POST.get('hora')
        salida = PS_registrarServicio(FECHA_SERVICIO,  ID_CLIENTE, ID_ESTADO_SERVICIO, id_motivo_visita, hora_servicio)
        if salida == 1:
            messages.success(request, "Visita Agendada Correctamente")
            data['mensaje'] = 'Visita Agendada'
            return redirect('home-calendar')
        else:
            data['mensaje'] = 'Error al Agendar Visita'
    return render(request, 'web/registro-servicios.html',data )



def PS_registrarServicio(FECHA_SERVICIO,  ID_CLIENTE, ID_ESTADO_SERVICIO, id_motivo_visita, hora_servicio):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('sp_agregar_servicio',[FECHA_SERVICIO,  ID_CLIENTE, ID_ESTADO_SERVICIO, id_motivo_visita, hora_servicio, salida])
    return salida.getvalue()

def home_calendar(request):
  
    id_profesional = request.user.id_prof.id_profesional
    cal = ""
   
    if request.method == 'GET':
        FECHA_SERVICIO = request.GET.get('fecha')
        cal = PS_listarCalendarProfesional(id_profesional)
     

    
    return render(request, 'web/home-calendar.html', {'cal': cal})


def PS_listarCalendarProfesional(id_profesional):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr=cursor.callproc('sp_listar_servicio_calendar_prof',[id_profesional, salida])

    return salida.getvalue()


def admin_calendar(request):
  
    
    cal = ""
   
    if request.method == 'GET':
        FECHA_SERVICIO = request.GET.get('fecha')
        cal = listado_servicio_calendar()
     
    
    
    return render(request, 'web/calendar-admin.html', {'cal': cal})


def listado_servicio_calendar():
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_SERVICIO_CALENDAR", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista




def listar_servicio_detalle(request,pk):
    servicio = Servicio.objects.get(id_servicio=pk)
    idservicio = servicio.id_servicio
    data = PS_buscarServicio(idservicio)
    
    

    return render(request, 'web/listar-servicio-detalle.html', {'data':data})


def listar_calendario_detalle_prof(request,pk):
    servicio = Servicio.objects.get(id_servicio=pk)
    idservicio = servicio.id_servicio
    data = PS_buscarServicio(idservicio)
    
    

    return render(request, 'web/listar-calendario-prof.html', {'data':data})

def PS_buscarServicio(ID_SERVICIO):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('SP_LISTAR_SERVICIO_ID',[ID_SERVICIO, salida])
  
    return salida.getvalue()


    





"""class Asiganar_Calender(TemplateView):

    def post(self,request, *args,**kwargs):

        data = {
        #'lista_tipo_servicio':listado_tipo_servicio(),
        'tipo_subtipo_servicio':listado_tipo_subtipo_servicio(),
        'listar_cliente':PS_listarCliente(),
        'listar_profesional':PS_listarProfesional(),
        'estado_servicio':listado_estado_servicio()
         }
        if request.method == 'POST':
        
          FECHA_SERVICIO = request.POST.get('Fecha')
          PRECIO = request.POST.get('Precio')
          ID_CLIENTE = request.POST.get('listar_cliente')
          ID_PROFESIONAL = request.POST.get('listar_profesional')
          ID_SUBTIPO_SERVICIO = request.POST.get('tipo_subtipo_servicio')
          ID_ESTADO_SERVICIO = request.POST.get('estado_servicio')
          salida = PS_registrarServicio(FECHA_SERVICIO, PRECIO, ID_CLIENTE, ID_PROFESIONAL, ID_SUBTIPO_SERVICIO, ID_ESTADO_SERVICIO)

          if salida == 1:
            data['mensaje'] = 'Agregado correctamente'
            return redirect('get')
          else:
            data['mensaje'] = 'Error al agregar'
        return render(request, 'web/prueba.html',data )




    def get(self,request, *args,**kwargs):
        cal = ""
   
        if request.method == 'GET':
          FECHA_SERVICIO = request.GET.get('fecha')
          cal = listado_servicio_calendar()
        return render(request, 'web/prueba.html', {'cal': cal})"""
    
   






def checkList1(request):
    checks = Checklist.objects.all()
    form = CheckForm()
    id_profesional = request.user.id_prof.id_profesional
    data = PS_listar_cliente(id_profesional)
    if request.method == 'POST':
        form = CheckForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, ('Item agregado al checklist'))
            return redirect('checklist')
        else:
            print("no hay mano")

    context = {'checks':checks, 'form':form,'data':data}
    return render(request, 'web/crear-checklist.html',context)

def listar_checklist(request):
    if request.method == 'POST':
        ID_CLIENTE = request.POST.get('id_cliente')
        check = Checklist.objects.raw('select * from checklist where id_cliente = %s',[ID_CLIENTE])
        return render(request,'web/listar-checklist.html',{'check':check})
    else:
        ID_CLIENTE = request.GET.get('id_cliente')
        print(ID_CLIENTE)
        check = Checklist.objects.raw('select * from checklist where id_cliente = %s',[ID_CLIENTE])
        return render(request,'web/listar-checklist.html',{'check':check,'ID_CLIENTE':ID_CLIENTE})

def tachar(request,pk):
    check = Checklist.objects.get(id=pk)
    check.resultado = True
    check.save()
    return redirect('listar-checklist')

def cancelar(request,pk):
    check = Checklist.objects.get(id=pk)
    check.resultado = False
    check.save()
    return redirect('listar-checklist')



def responderChecklist(request, pk):
    check = Checklist.objects.get(id=pk)
    form  = CheckForm(instance=check)
    if request.method == 'POST':
        form = CheckForm(request.POST, instance=check)
        if form.is_valid():
            form.save()
            return redirect('listar-checklist')

    context = {'form':form}
    return render(request, 'web/responder-checklist.html',context)


#---------------------------------------------------------------------------------#

def SP_listarTipoSolcitud():
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_TIPO_SOLICITUD", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista 

def SP_listarEstadoSolcitud():
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_ESTADO_SOLICITUD", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista   

def PS_registrarsolicitud(ID_CLIENTE, ID_PROFESIONAL, ID_TIPO_SOLICITUD, DETALLE, FECHA_CREACION, HORA_CREACION, ID_ESTADO_SOLICITUD):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_SOLICITUD',[ID_CLIENTE, ID_PROFESIONAL, ID_TIPO_SOLICITUD, DETALLE, FECHA_CREACION, HORA_CREACION, ID_ESTADO_SOLICITUD,salida])
    return salida.getvalue()

def crear_solicitud(request):
    id_profesional = request.user.id_prof.id_profesional
    
    data = {
    'tipo_solicitud':SP_listarTipoSolcitud(),
    'estado_solicitud':SP_listarEstadoSolcitud(),
    'cliente_id_prof': PS_listar_cliente(id_profesional)
    }

    if request.method == 'POST':
        ID_CLIENTE = request.POST.get('cliente_id_prof')
        ID_PROFESIONAL = request.POST.get('id_profesional')
        ID_TIPO_SOLICITUD =request.POST.get('tipo_solicitud')
        DETALLE = request.POST.get('detalle')
        FECHA_CREACION = request.POST.get('fecha')
        HORA_CREACION = request.POST.get('hora')
        ID_ESTADO_SOLICITUD = request.POST.get('estado_solicitud')
        salida= PS_registrarsolicitud(ID_CLIENTE,ID_PROFESIONAL,ID_TIPO_SOLICITUD,DETALLE, FECHA_CREACION, HORA_CREACION, ID_ESTADO_SOLICITUD)
        if salida == 1:
            print("agrego")
            messages.success(request, "Agregado correctamente")
            data['mensaje'] = 'Agregado correctamente'
            return redirect('listar-solicitud')
        else:
            print("no agrego")
            data['mensaje'] = 'Error al agregar'
    return render (request, 'web/crear-solicitud.html',data)

def PS_listarSolicitud(ID_PROFESIONAL,ID_CLIENTE):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('SP_LISTAR_SOLICITUD_RUT',[ID_PROFESIONAL,ID_CLIENTE, salida])
  
    return salida.getvalue()

def listar_solicitud(request):
    id_profesional = request.user.id_prof.id_profesional
    data = PS_listar_cliente(id_profesional)

    if request.method == 'POST':
        ID_CLIENTE = request.POST.get('id_cliente')
        ID_PROFESIONAL = request.user.id_prof.id_profesional
        check = PS_listarSolicitud(ID_PROFESIONAL,ID_CLIENTE)
        if ID_CLIENTE == "":
            check = PS_listarSolicitud2(ID_PROFESIONAL)
            return render(request,'web/listar-solicitud.html',{'check':check,'data':data})
    else:
        ID_PROFESIONAL = request.user.id_prof.id_profesional
        check = PS_listarSolicitud2(ID_PROFESIONAL)
        return render(request,'web/listar-solicitud.html',{'check':check,'data':data})
    return render(request,'web/listar-solicitud.html',{'check':check,'data':data})



def PS_registrarSituacionActual(SITUACION_ACTUAL,PROPUESTA_GENERAL,ID_CLIENTE):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_SITUACION_ACTUAL',[SITUACION_ACTUAL,PROPUESTA_GENERAL,ID_CLIENTE,salida])
    return salida.getvalue()


def ingresarSituacionActual(request):

    id_profesional = request.user.id_prof.id_profesional
    data = PS_listar_cliente(id_profesional)
    if request.method == 'POST':
        SITUACION_ACTUAL = request.POST.get('situacion')
        PROPUESTA_GENERAL = request.POST.get('propuesta')
        ID_CLIENTE = request.POST.get('id_cliente') 
        salida= PS_registrarSituacionActual(SITUACION_ACTUAL,PROPUESTA_GENERAL,ID_CLIENTE)
        if salida == 1:
            messages.success(request, "Agregado correctamente")
            print("agrego")
        else:
            print("no agrego")
    return render(request,'web/situacion-actual.html',{'data':data})

def PS_buscarActividad(ID_PROFESIONAL,ID_CLIENTE):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = django_cursor.connection.cursor()
    cursor.callproc('SP_LISTAR_ACTIVIDAD_RUT',[ID_PROFESIONAL,ID_CLIENTE, salida])

    lista = []
    for fila in salida:
        data = {
            'data':fila,
            'evidencia_imagen':str(base64.b64encode(fila[6].read()), 'utf-8')
        }
        lista.append(data)
    return lista

def PS_listarActividad(ID_PROFESIONAL):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = django_cursor.connection.cursor()
    cursor.callproc('SP_LISTAR_ACTIVIDAD',[ID_PROFESIONAL, salida])

    lista = []
    for fila in salida:
        data = {
            'data':fila,
            'evidencia_imagen':str(base64.b64encode(fila[6].read()), 'utf-8')
        }
        lista.append(data)
    return lista

def PS_registrarActividadMejora(ID_CLIENTE,ORIGEN, ACTIVIDAD, ESTADO):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_ACTIVIDAD_MEJORA',[ID_CLIENTE,ORIGEN, ACTIVIDAD, ESTADO,salida])
    return salida.getvalue()




def ingresarActividadMejora(request):
    id_profesional = request.user.id_prof.id_profesional
    data = PS_listar_cliente(id_profesional)

    if request.method == 'POST':
        ORIGEN = request.POST.get('origen')
        ACTIVIDAD = request.POST.get('actividad')
        ESTADO = request.POST.get('estado')
        ID_CLIENTE = request.POST.get('id_cliente_a') 
        salida= PS_registrarActividadMejora(ID_CLIENTE,ORIGEN, ACTIVIDAD, ESTADO)
        if salida == 1:
            messages.success(request, "Actividad Agregada Correctamente")
            print("agrego")
        else:
            messages.error(request, "Error al Agregar Actividad")
            print("no agrego")
    return render(request,'web/actividad-mejora.html',{'data':data})

def listar_actividad(request):
    id_profesional = request.user.id_prof.id_profesional
    data = PS_listar_cliente(id_profesional)
    if request.method == 'POST':
        ID_PROFESIONAL = request.user.id_prof.id_profesional
        ID_CLIENTE = request.POST.get('id_cliente')
        actividad = PS_buscarActividad(ID_PROFESIONAL,ID_CLIENTE) 
        if ID_CLIENTE == "":
            actividad = PS_listarActividad(ID_PROFESIONAL)
            return render(request,'web/listar-actividad.html',{'actividad':actividad,'data':data})
    else:
        ID_PROFESIONAL = request.user.id_prof.id_profesional
        actividad = PS_listarActividad(ID_PROFESIONAL) 
        return render(request,'web/listar-actividad.html',{'actividad':actividad,'data':data})
    return render(request,'web/listar-actividad.html',{'actividad':actividad,'data':data})

@csrf_exempt
def modificarEstadoActividad(request):
    id = request.POST.get('id','')
    type = request.POST.get('type','')
    value = request.POST.get('value','')
    actividad = ActividadMejora.objects.get(id_actividad=id)
    if type=="estado":
        actividad.estado =value
    actividad.save()
    return JsonResponse({"success":"Modificado"})

@login_required(login_url='login')
def listar_actividad_cliente(request):
    if request.method == "POST" :
        id_cliente = request.POST.get('id_cliente')
        cliente = Cliente.objects.get(id_cliente=id_cliente)
        profesional = cliente.id_profesional.id_profesional
        actividad = PS_buscarActividad(profesional,id_cliente)

        data = {
            'actividad':actividad
        }
        return render(request,'web/listar-actividad-cliente.html',data)
    return render(request,'web/listar-actividad-cliente.html')

def PS_modificarEvidenciaMejora(ID_ACTIVIDAD,EVIDENCIA_TEXTO, EVIDENCIA_IMAGEN):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_EVIDENCIA_ACTIVIDAD',[ID_ACTIVIDAD,EVIDENCIA_TEXTO, EVIDENCIA_IMAGEN,salida])
    return salida.getvalue()


def responderActividad(request,pk):
    actividad = ActividadMejora.objects.get(id_actividad=pk)
    data = {
    'id':actividad.id_actividad,
    'texto':actividad.evidencia_texto,
    'imagen': actividad.evidencia_imagen,
    }

    if request.method == 'POST':
        ID_ACTIVIDAD = request.POST.get('id')
        EVIDENCIA_TEXTO = request.POST.get('texto')
        EVIDENCIA_IMAGEN = request.FILES['imagen'].read()
        salida= PS_modificarEvidenciaMejora(ID_ACTIVIDAD,EVIDENCIA_TEXTO, EVIDENCIA_IMAGEN)
        if salida == 1:
            data['mensaje'] = 'Modificado correctamente'
            return redirect('listar-actividad-cliente')
        else:
            data['mensaje'] = 'Error al modificar'
    return render(request,'web/responder-actividad.html',data)


def editarChecklist(request, pk):
    check = Checklist.objects.get(id=pk)
    form  = CheckForm(instance=check)
    if request.method == 'POST':
        form = CheckForm(request.POST, instance=check)
        if form.is_valid():
            form.save()
            return redirect('listar-checklist')

    context = {'form':form}
    return render(request, 'web/editar-checklist.html',context)

@csrf_exempt
def mark_notification_as_readed(request):
    if not request.method == 'POST':
        return JsonResponse({})
    if not request.user.is_authenticated:
        return JsonResponse({})
    idp = request.user.id_prof.id_profesional
    profesional = Profesional.objects.get(id_profesional=idp)
    notifications = profesional.notificacion_asignada_a_profesional
    unreaded_notifications = notifications.filter(leido=False)
    for notification in unreaded_notifications.order_by('fecha_creacion'):
        notification.leido = True
        notification.save()
    return JsonResponse({'unreaded_notification_count':unreaded_notifications.count()})

@login_required(login_url='login')
def crearAlerta(request):
    alerta = Alerta.objects.all()
    form = AlertaForm()
    if request.method == "POST":
        form = AlertaForm(request.POST)
        if form.is_valid():
            form.save()
            print('Alerta agregada')
            return redirect('chat-room')
        else:
            print('no hay mano')
    context = {'alerta':alerta,'form':form}
    return render(request, 'web/crear-alerta.html',context)

@login_required(login_url='login')
def chat_room(request):
    return render(request, 'web/chat-room.html')

@login_required(login_url='login')
def room(request, room_name, person_name):

    return render(request,"web/chat-screen.html",{'room_name':room_name,'person_name':person_name})

#-------------------------------------#

def listado_tipo_capacitacion():
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_TIPO_CAPACITACION", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


def PS_registrarCapacitacion(ASISTENTES, MATERIALES,ID_SERVICIO,ID_TIPO_CAPACITACION):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_CAPACITACION',[ASISTENTES, MATERIALES,ID_SERVICIO,ID_TIPO_CAPACITACION,salida])
    return salida.getvalue()

def crear_capacitacion(request, pk):
    data = {
    'tipo_capacitacion':listado_tipo_capacitacion(),
    }

    if request.method == 'POST':
        ASISTENTES = request.POST.get('id_profesional')
        MATERIALES = request.POST.get('materiales')
        ID_SERVICIO = pk
        ID_TIPO_CAPACITACION = request.POST.get('tipo_capacitacion')
        salida= PS_registrarCapacitacion(ASISTENTES,MATERIALES,ID_SERVICIO,ID_TIPO_CAPACITACION)
        print(ASISTENTES,MATERIALES,ID_SERVICIO,ID_TIPO_CAPACITACION)
        if salida == 1:
            messages.success(request, "Capacitacion Agregada")
            print("agrego")
            data['mensaje'] = 'Agregado correctamente'
            return redirect('listar-capacitacion')   
        else:
            messages.error(request, "Error al agregar una capacitacion")
            print("no agrego")
            data['mensaje'] = 'Error al agregar'
    return render (request, 'web/crear-capacitacion.html',data)

def PS_registrarAccidente(ID_CLIENTE, FECHA, HORA, LUGAR_ACCIDENTE, TRABAJO_HABITUAL, TIENE_EXPERIENCIA, TAREA_AUTORIZACION, DESC_LESION, GRADO_LESION, CONTINGENCIA):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_INGRESAR_ACCIDENTE',[ID_CLIENTE, FECHA, HORA, LUGAR_ACCIDENTE, TRABAJO_HABITUAL, TIENE_EXPERIENCIA, TAREA_AUTORIZACION, DESC_LESION, GRADO_LESION, CONTINGENCIA,salida])
    return salida.getvalue()

def ingresar_accidente(request):
    id_profesional = request.user.id_prof.id_profesional
    data = PS_listar_cliente(id_profesional)

    if request.method == 'POST':
        CLIENTE = request.POST.get('id_cliente')
        FECHA = request.POST.get('fecha')
        HORA = request.POST.get('hora')
        LUGAR_ACCIDENTE = request.POST.get('lugar_accidente')
        TRABAJO_HABITUAL = request.POST.get('trabajo_habitual')
        TIENE_EXPERIENCIA = request.POST.get('tiene_experiencia')
        TAREA_AUTORIZACION = request.POST.get('tarea_autorizacion')
        DESC_LESION = request.POST.get('desc_lesion')
        GRADO_LESION = request.POST.get('grado_lesion')
        CONTINGENCIA = request.POST.get('contingencia')
        salida= PS_registrarAccidente(CLIENTE, FECHA, HORA, LUGAR_ACCIDENTE, TRABAJO_HABITUAL, TIENE_EXPERIENCIA, TAREA_AUTORIZACION, DESC_LESION, GRADO_LESION, CONTINGENCIA)
        if salida == 1:
            print("agrego")
            messages.success(request, "Accidente Ingresado")
        else:
            print("no agrego")
            messages.error(request, "Error al registrar accidente")
    return render (request, 'web/ingresar-accidente.html')

def PS_registrarAsesoriaAccidente(ID_SERVICIO, ID_PROFESIONAL, INSPECCION_LUGAR_ACCIDENTE, VERIFICAR_CONTRATO_ACCIDENTADO, PLANIFICAR_CAPACITACION_RIESGOS):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_ASESORIA_ACCIDENTE',[ID_SERVICIO, ID_PROFESIONAL, INSPECCION_LUGAR_ACCIDENTE, VERIFICAR_CONTRATO_ACCIDENTADO, PLANIFICAR_CAPACITACION_RIESGOS,salida])
    return salida.getvalue()


def crear_asesoria_accidente(request, pk):

    if request.method == 'POST':
        ID_SERVICIO = pk
        ID_PROFESIONAL = request.POST.get('id_profesional')
        INSPECCION_LUGAR_ACCIDENTE = request.POST.get('inspeccion')
        VERIFICAR_CONTRATO_ACCIDENTADO = request.POST.get('verificar_contrato')
        PLANIFICAR_CAPACITACION_RIESGOS = request.POST.get('planificar_capacitacion')
        salida= PS_registrarAsesoriaAccidente(ID_SERVICIO, ID_PROFESIONAL, INSPECCION_LUGAR_ACCIDENTE, VERIFICAR_CONTRATO_ACCIDENTADO, PLANIFICAR_CAPACITACION_RIESGOS)
        if salida == 1:
            messages.success(request, "Agregado correctamente")
            print("agrego")
            return redirect('listar-asesoria-accidente')
        else:
            messages.error(request, "Error al ingresar, intente nuevamente")
            print("no agrego")
    return render (request, 'web/ingresar-asesoria-accidente.html')

def listado_ente_fiscalizador():
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_ENTE_FISCALIZADOR", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def PS_registrarAsesoriaFiscalizacion(ID_SERVICIO, ENTE_FISCALIZADOR, FECHA_FISCALIZACION, DETALLE_EVENTO, JUICIO, CONVERSACION_FISCALIZADOR, EVIDENCIAR_DOCUMENTACION, CONTINGENCIA, ID_PROFESIONAL):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_ASESORIA_FISCALIZACION',[ID_SERVICIO, ENTE_FISCALIZADOR, FECHA_FISCALIZACION, DETALLE_EVENTO, JUICIO, CONVERSACION_FISCALIZADOR, EVIDENCIAR_DOCUMENTACION, CONTINGENCIA, ID_PROFESIONAL,salida])
    return salida.getvalue()

def crear_asesoria_fiscalizador(request, pk):
    data = {
    'ente_fiscalizador':listado_ente_fiscalizador(),
    }

    if request.method == 'POST':
        ID_SERVICIO = pk
        ENTE_FISCALIZADOR = request.POST.get('ente_fiscalizador')
        FECHA_FISCALIZACION = request.POST.get('fecha')
        DETALLE_EVENTO = request.POST.get('detalle')
        JUICIO = request.POST.get('juicio')
        CONVERSACION_FISCALIZADOR = request.POST.get('conversacion')
        EVIDENCIAR_DOCUMENTACION = request.POST.get('evidenciar')
        CONTINGENCIA = request.POST.get('contingencia')
        ID_PROFESIONAL = request.POST.get('id_profesional')      
        salida= PS_registrarAsesoriaFiscalizacion(ID_SERVICIO, ENTE_FISCALIZADOR, FECHA_FISCALIZACION, DETALLE_EVENTO, JUICIO, CONVERSACION_FISCALIZADOR, EVIDENCIAR_DOCUMENTACION, CONTINGENCIA, ID_PROFESIONAL)
        if salida == 1:
            print("agrego")
            data['mensaje'] = 'Agregado correctamente'
            messages.success(request, "Asesoria Agregada Correctamente")
            return redirect('listar-asesoria-fiscalizacion')

        else:

            print("no agrego")
            data['mensaje'] = 'Error al agregar'
            messages.error(request, "Error al Agregar")
    return render (request, 'web/ingresar-asesoria-fiscalizacion.html',data)

def PS_buscarAsesoriaAccidente(ID_PROFESIONAL,ID_CLIENTE):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('SP_LISTAR_ASESORIA_ACCIDENTE_FILTRO',[ID_PROFESIONAL,ID_CLIENTE, salida])

    return salida.getvalue()

def PS_listarAsesoriaAccidente(ID_PROFESIONAL):
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('SP_LISTAR_ASESORIA_ACCIDENTE',[ID_PROFESIONAL, salida])

    return salida.getvalue()

def listarAsesoriaAccidente(request):
    id_profesional = request.user.id_prof.id_profesional
    data = PS_listar_cliente(id_profesional)
    if request.method == 'POST':
        ID_PROFESIONAL = request.user.id_prof.id_profesional
        ID_CLIENTE = request.POST.get('id_cliente')
        salida = PS_buscarAsesoriaAccidente(ID_PROFESIONAL,ID_CLIENTE)
        if ID_CLIENTE == "":
            salida = PS_listarAsesoriaAccidente(ID_PROFESIONAL)
            return render(request,'web/listar-asesoria-accidente.html',{'salida':salida,'data':data})
    else:
        ID_PROFESIONAL = request.user.id_prof.id_profesional
        salida = PS_listarAsesoriaAccidente(ID_PROFESIONAL)
        return render(request,'web/listar-asesoria-accidente.html',{'salida':salida,'data':data})
    return render(request, 'web/listar-asesoria-accidente.html', {'salida':salida,'data':data})


def PS_modificarAsesoriaAccidente(ID_SERVICIO,ID_ESTADO_SERVICIO):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_ASESORIA_ACCIDENTE',[ID_SERVICIO,ID_ESTADO_SERVICIO,salida])
    return salida.getvalue()

def modificarAsesoriaAccidente(request,pk):
    servicio = Servicio.objects.get(id_servicio=pk)
    data = {
    'id_servicio': servicio.id_servicio,
    'id_estado': servicio.id_estado_servicio.id_estado_servicio,
    'estado_servicio': servicio.id_estado_servicio.descripcion,
    'eee': listado_estado_servicio(),
    }
    if request.method == 'POST':
        ID_SERVICIO= request.POST.get('id_servicio')
        ID_ESTADO_SERVICIO = request.POST.get('estado_servicio')
        salida= PS_modificarAsesoriaAccidente(ID_SERVICIO,ID_ESTADO_SERVICIO)
        if salida == 1:
            data['mensaje'] = 'Modificado correctamente'
            return redirect('listar-asesoria-accidente')
        else:
            data['mensaje'] = 'Error al modificar'
    return render(request, 'web/modificar-asesoria-accidente.html',data)


def PS_buscarAsesoriaFiscalizacion(ID_PROFESIONAL,ID_CLIENTE):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('SP_LISTAR_ASESORIA_FISCALIZACION_FILTRO',[ID_PROFESIONAL,ID_CLIENTE, salida])

    return salida.getvalue()

def PS_listarAsesoriaFiscalizacion(ID_PROFESIONAL):
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('SP_LISTAR_ASESORIA_FISCALIZACION',[ID_PROFESIONAL, salida])

    return salida.getvalue()

def listarAsesoriaFiscalizacion(request):
    id_profesional = request.user.id_prof.id_profesional
    data = PS_listar_cliente(id_profesional)

    if request.method == 'POST':
        ID_PROFESIONAL = request.user.id_prof.id_profesional
        ID_CLIENTE = request.POST.get('id_cliente')
        salida = PS_buscarAsesoriaFiscalizacion(ID_PROFESIONAL,ID_CLIENTE)
        if ID_CLIENTE == "":
            salida = PS_listarAsesoriaFiscalizacion(ID_PROFESIONAL)
            return render(request,'web/listar-asesoria-fiscalizacion.html',{'salida':salida,'data':data})
    else:
        ID_PROFESIONAL = request.user.id_prof.id_profesional
        salida = PS_listarAsesoriaFiscalizacion(ID_PROFESIONAL)
        return render(request,'web/listar-asesoria-fiscalizacion.html',{'salida':salida,'data':data})
    return render(request, 'web/listar-asesoria-fiscalizacion.html', {'salida':salida,'data':data})

def modificarAsesoriaFiscalizacion(request,pk):
    servicio = Servicio.objects.get(id_servicio=pk)
    data = {
    'id_servicio': servicio.id_servicio,
    'id_estado': servicio.id_estado_servicio.id_estado_servicio,
    'estado_servicio': servicio.id_estado_servicio.descripcion,
    'eee': listado_estado_servicio(),
    }
    if request.method == 'POST':
        ID_SERVICIO= request.POST.get('id_servicio')
        ID_ESTADO_SERVICIO = request.POST.get('estado_servicio')
        salida= PS_modificarAsesoriaAccidente(ID_SERVICIO,ID_ESTADO_SERVICIO)
        if salida == 1:
            data['mensaje'] = 'Modificado correctamente'
            return redirect('listar-asesoria-fiscalizacion')
        else:
            data['mensaje'] = 'Error al modificar'
    return render(request, 'web/modificar-asesoria-fiscalizacion.html',data)

####################################################################################
'''REPORTES'''
def reportAllclient(request):
    
    id_profesional = request.user.id_prof.id_profesional
    
    clien = ""
    if request.method == 'GET':
        ID_CLIENTE = request.GET.get('rut')
        clien = PS_listarClienteProf(id_profesional)
    return render(request,'web/reportes-all.html',{'clien':clien})

def reportAllclientAdmin(request):
    
    
    
    clien = ""
    if request.method == 'GET':
        ID_CLIENTE = request.GET.get('rut')
        clien = PS_listarCliente()
    return render(request,'web/reportes-all-admin.html',{'clien':clien})






def PS_listarClienteProf(id_profesional):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr=cursor.callproc('sp_listar_cliente_profesional_id',[id_profesional, salida])

    return salida.getvalue()

# REPORTE DE LA SITUACION ACTUAL
class reporteSituacionActualView(View):
    def get(self,request,*args,**kwargs):
        try:
            template = get_template('web/reporte-situacion-actual.html')
            cli = Cliente.objects.get(pk=self.kwargs['pk'])
            idc = cli.id_cliente
            context = {
                'cliente': Cliente.objects.get(pk=self.kwargs['pk']),
                'check': Checklist.objects.filter(id_cliente=idc),
                'situacion': SituacionActual.objects.filter(id_cliente=idc),
                'actividad': ActividadMejora.objects.filter(id_cliente=idc,origen='Checklist')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            filename= cli.id_cliente
            response['Content-Disposition'] = 'attachment; filename="reporte_situacion' + filename + '.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('report-all'))

@login_required(login_url='login')
def pdfSituacionActual_view(request):
    with open('C:/Users/Janitro/Downloads/reporte_situacion'+request.user.id_cliente.id_cliente+'.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'filename=some_file.pdf'
        return response

@login_required(login_url='login')
def templateReportSituacion(request):
    return render(request,'web/ver-reportes-situacion.html')
# FIN DEL REPORTE DE SITUACION ACTUAL

# REPORTE DE LAS VISITAS
class reporteVisita(View):
    def get(self,request,*args,**kwargs):
        try:
            template = get_template('web/reporte-visitas.html')
            cli = Cliente.objects.get(pk=self.kwargs['pk'])
            idc = cli.id_cliente
            context = {
                'cliente': Cliente.objects.get(pk=self.kwargs['pk']),
                'visita': Servicio.objects.filter(id_cliente=idc),
                'total': Servicio.objects.filter(id_cliente=idc).count(),
                'pendiente': Servicio.objects.filter(id_cliente=idc,id_estado_servicio= 1).count(),
                'proceso': Servicio.objects.filter(id_cliente=idc,id_estado_servicio= 2).count(),
                'finalizado': Servicio.objects.filter(id_cliente=idc,id_estado_servicio= 3).count(),
                'checklist': Servicio.objects.filter(id_cliente=idc,id_motivo_visita= 2).count(),
                'capacitacion': Servicio.objects.filter(id_cliente=idc,id_motivo_visita= 3).count(),
                'accidente': Servicio.objects.filter(id_cliente=idc,id_motivo_visita= 4).count(),
                'fiscalizacion': Servicio.objects.filter(id_cliente=idc,id_motivo_visita= 5).count()
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            filename= cli.id_cliente
            response['Content-Disposition'] = 'attachment; filename="reporte_visitas' + filename + '.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('report-all'))


@login_required(login_url='login')
def pdfVisitas_view(request):
    with open('C:/Users/Janitro/Downloads/reporte_visitas'+request.user.id_cliente.id_cliente+'.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'filename=some_file.pdf'
        return response

@login_required(login_url='login')
def templateReportVisitas(request):
    return render(request,'web/ver-reporte-visitas.html')
# FIN DEL REPORTE DE LAS VISITAS

# REPORTE DE LAS CAPACITACIONES
def PS_buscarResultadoCapacitacion(ID_CLIENTE):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('SP_LISTAR_RESULTADO_RUT_CAPACITACION',[ID_CLIENTE, salida])
  
    return salida.getvalue()

class reporteCapacitacion(View):
    def get(self,request,*args,**kwargs):
        try:
            template = get_template('web/reporte-capacitacion.html')
            cli = Cliente.objects.get(pk=self.kwargs['pk'])
            idc = cli.id_cliente
            profesional = cli.id_profesional.id_profesional
            capacitacion = PS_buscarCapacitacion(profesional,idc)
            resultado = PS_buscarResultadoCapacitacion(idc)
            html = template.render({'cliente':cli,'capacitacion':capacitacion,'resultado':resultado})
            response = HttpResponse(content_type='application/pdf')
            filename= cli.id_cliente
            response['Content-Disposition'] = 'attachment; filename="reporte_capacitacion' + filename + '.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('report-all'))

@login_required(login_url='login')
def pdfCapacitacion_view(request):
    with open('C:/Users/Janitro/Downloads/reporte_capacitacion'+request.user.id_cliente.id_cliente+'.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'filename=some_file.pdf'
        return response

@login_required(login_url='login')
def templateReportCapacitacion(request):
    return render(request,'web/ver-reportes-capacitacion.html')
# FIN DEL REPORTE DE LAS CAPACITACIONES

#REPORTE DE LAS ASESORIAS POR ACCIDENTE
def PS_buscarResultadoAccidente(ID_CLIENTE):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('SP_LISTAR_RESULTADO_RUT_ACCIDENTE',[ID_CLIENTE, salida])
  
    return salida.getvalue()

class reporteAsesoriaAccidente(View):
    def get(self,request,*args,**kwargs):
        try:
            template = get_template('web/reporte-asesoria-accidente.html')
            cli = Cliente.objects.get(pk=self.kwargs['pk'])
            idc = cli.id_cliente
            profesional = cli.id_profesional.id_profesional
            asesoria = PS_buscarAsesoriaAccidente(profesional,idc)
            accidentes = Accidente.objects.filter(id_cliente=idc)
            count = Accidente.objects.filter(id_cliente=idc).count()
            resultado = PS_buscarResultadoAccidente(idc)
            html = template.render({'cliente':cli,'asesoria':asesoria,'accidente':accidentes,'resultado':resultado,'count':count})
            response = HttpResponse(content_type='application/pdf')
            filename= cli.id_cliente
            response['Content-Disposition'] = 'attachment; filename="reporte_accidente' + filename + '.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('report-all'))

@login_required(login_url='login')
def pdfAccidente_view(request):
    with open('C:/Users/Janitro/Downloads/reporte_accidente'+request.user.id_cliente.id_cliente+'.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'filename=some_file.pdf'
        return response

@login_required(login_url='login')
def templateReportAccidente(request):
    return render(request,'web/ver-reportes-accidentes.html')
# FIN DEL REPORTE DE ASESORIAS POR ACCIDENTES 

# REPORTE DE LAS ASESORIAS POR FISCALIZACION

def PS_buscarFiscalizacion(ID_CLIENTE):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('SP_LISTAR_ASESORIA_FISCALIZACION_REPORTE',[ID_CLIENTE, salida])
  
    return salida.getvalue()

def PS_buscarResultadoFiscalizacion(ID_CLIENTE):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('SP_LISTAR_RESULTADO_RUT_FISCALIZACION',[ID_CLIENTE, salida])
  
    return salida.getvalue()

class reporteAsesoriaFiscalizacion(View):
    def get(self,request,*args,**kwargs):
        try:
            template = get_template('web/reporte-asesoria-fiscalizacion.html')
            cli = Cliente.objects.get(pk=self.kwargs['pk'])
            idc = cli.id_cliente
            asesoria = PS_buscarFiscalizacion(idc)
            resultado = PS_buscarResultadoFiscalizacion(idc)
            html = template.render({'cliente':cli,'asesoria':asesoria,'resultado':resultado})
            response = HttpResponse(content_type='application/pdf')
            filename= cli.id_cliente
            response['Content-Disposition'] = 'attachment; filename="reporte_fiscalizacion' + filename + '.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('report-all'))

@login_required(login_url='login')
def pdfFiscalizacion_view(request):
    with open('C:/Users/Janitro/Downloads/reporte_fiscalizacion'+request.user.id_cliente.id_cliente+'.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'filename=some_file.pdf'
        return response

@login_required(login_url='login')
def templateReportFiscalizacion(request):
    return render(request,'web/ver-reportes-fiscalizacion.html')
# FIN DE LOS REPORTES DE ASESORIA POR FISCALIZACIÓN

# REPORTE DE LAS SOLICITUDES DEL CLIENTE
def PS_buscarSolicitud(ID_CLIENTE):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('SP_LISTAR_SOLICITUD_REPORTE',[ID_CLIENTE, salida])
  
    return salida.getvalue()

class reporteSolicitud(View):
    def get(self,request,*args,**kwargs):
        try:
            template = get_template('web/reporte-solicitud.html')
            cli = Cliente.objects.get(pk=self.kwargs['pk'])
            idc = cli.id_cliente
            context = {
                'cliente' : Cliente.objects.get(pk=self.kwargs['pk']),
                'solicitud' : PS_buscarSolicitud(idc),
                'count_llamadas' : Solicitud.objects.filter(id_cliente=idc, id_tipo_solicitud=3).count,
                'count_check' : Solicitud.objects.filter(id_cliente=idc, id_tipo_solicitud=1).count,
                'count_cap' : Solicitud.objects.filter(id_cliente=idc, id_tipo_solicitud=2).count,
                'count_doc' : Solicitud.objects.filter(id_cliente=idc, id_tipo_solicitud=6).count,
                'count_accid' : Solicitud.objects.filter(id_cliente=idc, id_tipo_solicitud=4).count,
                'count_fisc' : Solicitud.objects.filter(id_cliente=idc, id_tipo_solicitud=5).count
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            filename= cli.id_cliente
            response['Content-Disposition'] = 'attachment; filename="reporte_solicitud' + filename + '.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('report-all'))

@login_required(login_url='login')
def pdfSolicitud_view(request):
    with open('C:/Users/Janitro/Downloads/reporte_solicitud'+request.user.id_cliente.id_cliente+'.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'filename=some_file.pdf'
        return response

@login_required(login_url='login')
def templateReportSolicitud(request):
    return render(request,'web/ver-reportes-solicitud.html')
# FIN REPORTES DE SOLICITUD

def PS_listarCapacitacion(ID_PROFESIONAL):
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('SP_LISTAR_CAPACITACION',[ID_PROFESIONAL, salida])

    return salida.getvalue()


def PS_buscarCapacitacion(ID_PROFESIONAL,ID_CLIENTE):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('SP_LISTAR_CAPACITACION_RUT',[ID_PROFESIONAL,ID_CLIENTE, salida])

    return salida.getvalue()

def listarCapacitacion(request):
    id_profesional = request.user.id_prof.id_profesional
    data = PS_listar_cliente(id_profesional)

    if request.method == 'POST':
        ID_PROFESIONAL = request.user.id_prof.id_profesional
        ID_CLIENTE = request.POST.get('id_cliente')
        salida = PS_buscarCapacitacion(ID_PROFESIONAL,ID_CLIENTE)
        if ID_CLIENTE == "":
            salida = PS_listarCapacitacion(ID_PROFESIONAL)
            return render(request,'web/listar-capacitacion.html',{'salida':salida,'data':data})
    else:
        ID_PROFESIONAL = request.user.id_prof.id_profesional
        salida = PS_listarCapacitacion(ID_PROFESIONAL)
        return render(request,'web/listar-capacitacion.html',{'salida':salida,'data':data})
    return render(request, 'web/listar-capacitacion.html', {'salida':salida,'data':data})

def PS_registrarResultado(ID_SERVICIO, FECHA_FINALIZACION, ANALISIS, RESULTADO, AREAS_OPORTUNIDAD):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_RESULTADO',[ID_SERVICIO, FECHA_FINALIZACION, ANALISIS, RESULTADO, AREAS_OPORTUNIDAD,salida])
    return salida.getvalue()


def registrarResultado(request,pk):

    if request.method == 'POST':
        id_servicio = pk
        FECHA_FINALIZACION = request.POST.get('fecha')
        ANALISIS = request.POST.get('analisis')
        resultado = request.POST.get('resultado')
        AREAS_OPORTUNIDAD = request.POST.get('oportunidad')
        salida = PS_registrarResultado(id_servicio,FECHA_FINALIZACION,ANALISIS,resultado,AREAS_OPORTUNIDAD)
        if salida == 1:
            print("agrego")

            return redirect('listar-resultado')
        else:
            print("no agregó")
            return render(request,'web/registrar-resultado.html')
    return render(request,'web/registrar-resultado.html')

def PS_listarResultado(ID_PROFESIONAL):
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('SP_LISTAR_RESULTADO',[ID_PROFESIONAL, salida])

    return salida.getvalue()

def PS_buscarResultado(ID_PROFESIONAL,ID_CLIENTE):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('SP_LISTAR_RESULTADO_RUT',[ID_PROFESIONAL,ID_CLIENTE, salida])
    
    return salida.getvalue()

def listarResultado(request):

    id_profesional = request.user.id_prof.id_profesional
    data = PS_listar_cliente(id_profesional)
    if request.method == 'POST':
        ID_PROFESIONAL = request.user.id_prof.id_profesional
        ID_CLIENTE = request.POST.get('id_cliente')
        salida = PS_buscarResultado(ID_PROFESIONAL,ID_CLIENTE)
        if ID_CLIENTE == "":
            salida = PS_listarResultado(ID_PROFESIONAL)
            return render(request,'web/listar-resultado.html',{'salida':salida,'data':data})
    else:
        ID_PROFESIONAL = request.user.id_prof.id_profesional
        salida = PS_listarResultado(ID_PROFESIONAL)
        return render(request,'web/listar-resultado.html',{'salida':salida,'data':data})
    return render(request, 'web/listar-resultado.html', {'salida':salida,'data':data})

def PS_registrarResultado(ID_SERVICIO, FECHA_FINALIZACION, ANALISIS, RESULTADO, AREAS_OPORTUNIDAD):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_RESULTADO',[ID_SERVICIO, FECHA_FINALIZACION, ANALISIS, RESULTADO, AREAS_OPORTUNIDAD,salida])
    return salida.getvalue()


def registrarResultado(request,pk):

    if request.method == 'POST':
        id_servicio = pk
        FECHA_FINALIZACION = request.POST.get('fecha')
        ANALISIS = request.POST.get('analisis')
        resultado = request.POST.get('resultado')
        AREAS_OPORTUNIDAD = request.POST.get('oportunidad')
        salida = PS_registrarResultado(id_servicio,FECHA_FINALIZACION,ANALISIS,resultado,AREAS_OPORTUNIDAD)
        if salida == 1:
            print("agrego")
            messages.success(request,"Resultado Registrado ")
            return redirect('listar-resultado')
        else:
            print("no agregó")
            messages.error(request,"Error al Registrar Resultado")
            return render(request,'web/registrar-resultado.html')
    return render(request,'web/registrar-resultado.html')


def PS_buscarCliente(ID_CLIENTE):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('SP_LISTAR_CLIENTE_RUT',[ID_CLIENTE, salida])

    return salida.getvalue()

def PS_listarSolicitud2(ID_PROFESIONAL):
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)

    pr = cursor.callproc("SP_LISTAR_SOLICITUD", [ID_PROFESIONAL, salida])

    return salida.getvalue()

def PS_modificarSolicitud(ID_SOLICITUD,ID_ESTADO_SOLICITUD):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_ESTADO_SOLICITUD',[ID_SOLICITUD,ID_ESTADO_SOLICITUD,salida])
    return salida.getvalue()

def modificarEstadoSolicitud(request,pk):
    solicitud = Solicitud.objects.get(id_solicitud=pk)
    data = {
    'id_solicitud': solicitud.id_solicitud,
    'id_estado': solicitud.id_estado_solicitud.id_estado_solicitud,
    'estado_solicitud': solicitud.id_estado_solicitud.estado_solicitud,
    'eee': SP_listarEstadoSolcitud(),
    }
    if request.method == 'POST':
        ID_SOLICITUD= request.POST.get('id_solicitud')
        ID_ESTADO_SOLICITUD = request.POST.get('estado_solicitud')
        salida= PS_modificarSolicitud(ID_SOLICITUD,ID_ESTADO_SOLICITUD)
        if salida == 1:
            data['mensaje'] = 'Modificado correctamente'
            return redirect('listar-solicitud')
        else:
            data['mensaje'] = 'Error al modificar'
    return render(request, 'web/modificar-estado-solicitud.html',data)

def PS_modificarEstadoCapacitacion(ID_SERVICIO,ID_ESTADO_SERVICIO):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_MODIFICAR_CAPACITACION',[ID_SERVICIO,ID_ESTADO_SERVICIO,salida])
    return salida.getvalue()

def modificarEstadoCapacitacion(request,pk):
    servicio = Servicio.objects.get(id_servicio=pk)
    data = {
    'id_servicio': servicio.id_servicio,
    'id_estado': servicio.id_estado_servicio.id_estado_servicio,
    'estado_servicio': servicio.id_estado_servicio.descripcion,
    'eee': listado_estado_servicio(),
    }
    if request.method == 'POST':
        ID_SERVICIO= request.POST.get('id_servicio')
        ID_ESTADO_SERVICIO = request.POST.get('estado_servicio')
        salida= PS_modificarEstadoCapacitacion(ID_SERVICIO,ID_ESTADO_SERVICIO)
        if salida == 1:
            data['mensaje'] = 'Modificado correctamente'
            return redirect('listar-capacitacion')
        else:
            data['mensaje'] = 'Error al modificar'
    return render(request, 'web/modificar-capacitacion.html',data)

def send_email(email,clave,nombre):
    context = {'email':email,'pass':clave,'nombre':nombre}
    template = get_template('web/correo.html')
    content  = template.render(context)

    mail = EmailMultiAlternatives(
        'Contraseña para su cuenta',
        'Bienvenido',
        settings.EMAIL_HOST_USER,
        [email]
    )

    mail.attach_alternative(content, 'text/html')
    mail.send()

def PS_listarSolicitudAdmin(ID_CLIENTE):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('SP_LISTAR_SOLICITUD_ADMIN_RUT',[ID_CLIENTE, salida])

    return salida.getvalue()

def PS_listarSolicitudAdmin2():
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_SOLICITUD_ADMIN", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def listar_solicitud_admin(request):
    if request.method == 'POST':
        ID_CLIENTE = request.POST.get('id_cliente')
        check = PS_listarSolicitudAdmin(ID_CLIENTE)
        if ID_CLIENTE == "":
            check = PS_listarSolicitudAdmin2()
            return render(request,'web/listar-solicitud-admin.hadmtml',{'check':check})
    else:
        check = PS_listarSolicitudAdmin2()
        return render(request,'web/listar-solicitud-admin.html',{'check':check})
    return render(request,'web/listar-solicitud-admin.html',{'check':check})

def PS_listar_cliente(ID_PROFESIONAL):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('SP_LISTAR_CLIENTE',[ID_PROFESIONAL,salida])
    return salida.getvalue()



#fabian

class CheckViewSet(viewsets.ModelViewSet):
    queryset  = Checklist.objects.all().order_by('-id')
    serializer_class = CheckSerial

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            pk=self.kwargs['pk'],
        )
        return obj



class ClienteviewSet(viewsets.ModelViewSet):
    queryset  = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            pk=self.kwargs['pk'],
        )
        return obj


class ServicioviewSet(viewsets.ModelViewSet):
    queryset  = Servicio.objects.all()
    serializer_class = ServicioSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            pk=self.kwargs['pk'],
        )
        return obj


class SearchCalendar(ListAPIView):
    queryset = Servicio.objects.all().order_by('-fecha_servicio')
    
    serializer_class = ServicioSerializer
    filter_backends = (SearchFilter ,OrderingFilter)
    search_fields = ('fecha_servicio','hora_servicio', 'id_cliente__nombre_empresa', 'id_motivo_visita__tipo_visita', 'id_estado_servicio__descripcion' )

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            pk=self.kwargs['pk'],
        )
        return obj


class SearchVisitas(ListAPIView):
    queryset = Cliente.objects.all()
    
    serializer_class = ClienteSerializer
    filter_backends = (SearchFilter ,OrderingFilter)
    search_fields = ('id_cliente','nombre_empresa', 'email_cliente', 'direccion', 'servicio_activo' )

class SearchSolcitud(ListAPIView):
    queryset = Solicitud.objects.all().order_by('-fecha_creacion') 
    
    serializer_class = SolicitudSerializer
    filter_backends = (SearchFilter ,OrderingFilter)
    search_fields = ('id_solicitud', 'id_cliente__nombre_empresa', 'id_profesional', 'id_tipo_solicitud__tipo_solicitud', 'detalle', 'fecha_creacion', 'hora_creacion','id_estado_solicitud__estado_solicitud')


#PAGOS

def pagos_admin(request):
    
    ID_CLIENTE = ""
    if request.method == 'POST':
        ID_CLIENTE = request.POST.get('rut')
        salida = PS_RegistrarPagos(ID_CLIENTE)
        print("Bien")
        if salida == 1:
            print("Registrado")
            messages.success(request, "Pago ingresado")
            salida = PS_listarFactura()

        elif salida == 0:
            print("Cliente no tiene deuda")   
            messages.error(request, "Cliente No Tiene Deuda ")
            salida = PS_listarFactura()
        
        
        else:
            print("Error")
            messages.error(request, "Cliente no existe")
            salida = PS_listarFactura()
        return render(request,'web/pagos-admin.html',{'salida':salida})
        
       
       

    else:
        print("REFRESHHH MEN")
        
        salida = PS_listarFactura()
        return render(request,'web/pagos-admin.html',{'salida':salida})
    
    
        
    return render(request, 'web/pagos-admin.html')
    
 
           

    

   



def PS_RegistrarPagos(ID_CLIENTE):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('sp_registrar_pago',[ID_CLIENTE, salida])

    return salida.getvalue()




def PS_listarFactura():
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_factura", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


#anidados



def PS_listar_comuna_por_region (id_region):
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_comuna_por_region", [out_cur, id_region])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista


def PS_listarRegion():
    django_cursor = connection.cursor()
    cursor= django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("sp_listar_region", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def comuna_por_region(request):
    

    region = request.GET.get('region')
    data = {
    'comunas':PS_listar_comuna_por_region(region)

    }

    return render(request, 'web/combox_regiones.html' , data)



def Visitas_para_clientes(request,pk):

    cliente = Cliente.objects.get(id_cliente=pk)
    idcliente = cliente.id_cliente
    data = PS_buscarVisitaCLiente(idcliente)
    

    return render(request, 'web/calendar-cliente.html', {'data':data})


def listar_servicio_detalle_cliente(request,pk):
    servicio = Servicio.objects.get(id_servicio=pk)
    idservicio = servicio.id_servicio
    data = PS_buscarServicio(idservicio)
    
    

    return render(request, 'web/listar-calendario-cliente.html', {'data':data})




def PS_buscarVisitaCLiente(ID_CLIENTE):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('sp_listar_calendario_cliente',[ID_CLIENTE, salida])

    return salida.getvalue()


def pagos_cliente(request,pk):
    
    cliente = Cliente.objects.get(id_cliente=pk)
    idcliente = cliente.id_cliente
    data = PS_PagoCliente(idcliente)
    
    
    return render(request, 'web/pagos-cliente.html', {'data':data})


def PS_PagoCliente(ID_CLIENTE):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('sp_listar_detalle_factura',[ID_CLIENTE, salida])

    return salida.getvalue()



# jenny sabado

def modificarEstadoSolicitudAdmin(request,pk):
    solicitud = Solicitud.objects.get(id_solicitud=pk)
    data = {
    'id_solicitud': solicitud.id_solicitud,
    'id_estado': solicitud.id_estado_solicitud.id_estado_solicitud,
    'estado_solicitud': solicitud.id_estado_solicitud.estado_solicitud,
    'eee': SP_listarEstadoSolcitud(),
    }
    if request.method == 'POST':
        ID_SOLICITUD= request.POST.get('id_solicitud')
        ID_ESTADO_SOLICITUD = request.POST.get('estado_solicitud')
        salida= PS_modificarSolicitud(ID_SOLICITUD,ID_ESTADO_SOLICITUD)
        if salida == 1:
            data['mensaje'] = 'Modificado correctamente'
            return redirect('listar-solicitud-admin')
        else:
            data['mensaje'] = 'Error al modificar'
    return render(request, 'web/modificar-estado-solicitud-admin.html',data)