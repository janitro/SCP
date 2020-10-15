from django.shortcuts import render
from django.db import connection 
import cx_Oracle
from web.models import Profesional

# Create your views here.
def home(request):
    return render(request, 'web/001home.html', {})

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
    }
    if request.method == 'POST':
        ID_PROFESIONAL = request.POST.get('id')
        NOMBRE_COMPLETO = request.POST.get('nombre')
        EMAIL_PROF = request.POST.get('email')
        PASSWORD_PROF = request.POST.get('password')
        ID_COMUNA = request.POST.get('comuna')
        DIRECCION = request.POST.get('direccion')
        TELEFONO_PROF = request.POST.get('telefono')
        ESTADO= request.POST.get('estado')
        ID_TIPO_PROFESIONAL = request.POST.get('tipoprof')
        CONTRATO_ACTIVO = request.POST.get('contrato')
        salida= registrarProfesional1(ID_PROFESIONAL,NOMBRE_COMPLETO, EMAIL_PROF, PASSWORD_PROF, ID_COMUNA, DIRECCION, TELEFONO_PROF, ESTADO, ID_TIPO_PROFESIONAL, CONTRATO_ACTIVO)
        if salida == 1:
            data['mensaje'] = 'Agregado correctamente'
        else:
            data['mensaje'] = 'Error al agregar'

    return render(request, 'web/registrarProfesional.html',data)

#Función para llamar el procedimiento de agregar profesional, el cual recibe como parametro las variables de arriba
def registrarProfesional1(ID_PROFESIONAL,NOMBRE_COMPLETO, EMAIL_PROF, PASSWORD_PROF, ID_COMUNA, DIRECCION, TELEFONO_PROF, ESTADO, ID_TIPO_PROFESIONAL, CONTRATO_ACTIVO):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_PROFESIONAL',[ID_PROFESIONAL,NOMBRE_COMPLETO, EMAIL_PROF, PASSWORD_PROF, ID_COMUNA, DIRECCION, TELEFONO_PROF, ESTADO, ID_TIPO_PROFESIONAL, CONTRATO_ACTIVO,salida])
    return salida.getvalue()

###############################################################
#DE ACA PARA ABAJO, JUNTO CON EL HTML "listarProfesional.html" aún no funcionan
################################################################
def ls(request):
    if request.method == 'POST':
        ID_PROFESIONAL = request.POST.get('rut')
        salida = listadoProfesional(ID_PROFESIONAL)
        data = {'prof':salida}
        if salida == 1:
            data['mensaje'] = 'Agregado correctamente'
        else:
            data['mensaje'] = 'Error al agregar'

    return render(request, 'web/listarProfesional.html')

def listadoProfesional(ID_PROFESIONAL):
    django_cursor =  connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.CURSOR)
    pr = cursor.callproc('SP_LISTAR_PROFESIONAL',[ID_PROFESIONAL, salida])
    print(salida)
    return salida.getvalue()
