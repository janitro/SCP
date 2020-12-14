from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer, WebsocketConsumer
from .models import *
from django.core import serializers
from channels.exceptions import StopConsumer
import json

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def websocket_connect(self, event):
        print("CONNECTED", event)

        await self.channel_layer.group_add(
            f"notification_group_{self.scope['url_route']['kwargs']['user_id']}",
            self.channel_name
        )

        await self.accept()
        
        context = await self.get_notification_info(self.scope)

        await self.send_json(content=context)

    async def websocket_disconnect(self, event):
        print("DISCONNECTED", event)
        await self.close()
        raise StopConsumer()


    async def websocket_receive(self, event):
        print("RECEIVE", event)
        await self.send(text_data='HELLO')

    async def notification_info(self,event):
        context = await self.get_notification_info(self.scope)

        await self.send_json(content=context)

    
    @database_sync_to_async
    def get_notification_info(self,scope):
        if not scope['user'].is_authenticated:
            context = {
                'unreaded_notification_count':'',
                'unreaded_notifications':'',
                'old_notifications':''
            }
            return context

        user = self.scope['user']
        idp = user.id_prof.id_profesional
        us = Profesional.objects.get(id_profesional=idp)
        notifications = us.notificacion_asignada_a_profesional.order_by('fecha_creacion')
        old_notifications = notifications.filter(leido=True)
        unreaded_notifications = notifications.filter(leido=False).order_by('fecha_creacion')

        context = {
            'unreaded_notification_count':unreaded_notifications.count(),
            'unreaded_notifications':serializers.serialize('json',unreaded_notifications),
            'old_notifications':serializers.serialize('json',old_notifications[:3])
        }

        return context

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.person_name = self.scope['url_route']['kwargs']['person_name']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': self.person_name+" se ha unido al chat"
            }
        )

        self.accept()

    def disconnect(self, code):
        # Leave room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type":"chat_message",
                "message": self.person_name+" dejo el chat"
            }
        )

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':self.person_name+" : "+message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))