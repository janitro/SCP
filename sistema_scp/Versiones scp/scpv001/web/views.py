from django.shortcuts import render, redirect
from django.db import connection 
import cx_Oracle
from web.models import Profesional, Comuna

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
    'com': profesionall.id_comuna,
    'direccion': profesionall.direccion,
    'telefono': profesionall.telefono_prof,
    'estado': profesionall.estado,
    'tipo': profesionall.id_tipo_profesional,
    'contrato': profesionall.contrato_activo
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
        salida= PS_modificarProfesional(ID_PROFESIONAL,NOMBRE_COMPLETO, EMAIL_PROF, PASSWORD_PROF, ID_COMUNA, DIRECCION, TELEFONO_PROF, ESTADO, ID_TIPO_PROFESIONAL, CONTRATO_ACTIVO)
        print(ID_PROFESIONAL,NOMBRE_COMPLETO, EMAIL_PROF, PASSWORD_PROF, ID_COMUNA, DIRECCION, TELEFONO_PROF, ESTADO, ID_TIPO_PROFESIONAL, CONTRATO_ACTIVO)
        if salida == 1:
            data['mensaje'] = 'Modificado correctamente'
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