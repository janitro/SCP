
from web.models import  *
from .models import *
from rest_framework import serializers
from rest_framework import viewsets, generics, status
from datetime import datetime






class CheckSerial(serializers.ModelSerializer):

	class Meta:
		model = Checklist
		fields = ('id', 'checklist', 'resultado', 'id_cliente')

class EstadoServicioSerializer(serializers.ModelSerializer):

	class Meta:
		model = EstadoServicio
		fields = ('id_estado_servicio', 'descripcion')

class MotivoSerializer (serializers.ModelSerializer):

	class Meta:
		model = MotivoVisita
		fields = ('id_motivo_visita', 'tipo_visita')




class ServicioSerializer(serializers.ModelSerializer):
	#fecha_servicio = serializers.DateTimeField(format="%d-%m-%Y", required=False, read_only=True)
	
	


	class Meta:
		model = Servicio

		fields = ('id_servicio', 'fecha_servicio', 'id_cliente', 'id_estado_servicio', 'id_motivo_visita', 'hora_servicio')


class ClienteSerializer(serializers.ModelSerializer):

	servicio = ServicioSerializer(many=True, read_only=True)

	class Meta:
		model = Cliente
        
		fields = ('id_cliente','nombre_empresa', 'email_cliente', 'direccion', 'servicio_activo','servicio')


class SolicitudSerializer(serializers.ModelSerializer):
	
	
	class Meta:
		model = Solicitud

		fields = ('id_solicitud', 'id_cliente', 'id_profesional', 'id_tipo_solicitud', 'detalle', 'fecha_creacion', 'hora_creacion','id_estado_solicitud')

		


