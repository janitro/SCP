from django.dispatch import receiver
from django.db.models.signals import post_save
from web.models import Alerta, Notificacion
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Alerta)
def create_notification(instance,*args, **kwargs):
    if kwargs['created']:
        Notificacion.objects.create(
            asignado_a= instance.asignado_a,
            descripcion=f"La empresa {instance.creado_por.nombre_empresa} ah generado una alerta de accidente!",
            pk_relacion=instance.id_alerta
        )
    else:
        if instance.creado_por != instance.asignado_a:
            if instance.respondido != instance.antigua_instancia.respondido:
                Notificacion.objects.create(
                    asignado_a_c= instance.asignado_a_c,
                    descripcion=f"Tu alerta con ID: {instance.id_alerta} cambio su estado ah {instance.respondido}",
                    pk_relacion=instance.id_alerta
                )

@receiver(post_save, sender=Notificacion)
def send_notification_info(*args, **kwargs):
    if kwargs['created']:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notification_group_{kwargs['instance'].asignado_a.id_profesional}", {
                'type':'notification_info'
            }
        )