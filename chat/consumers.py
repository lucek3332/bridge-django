# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user = self.scope['user']._wrapped
        self.author = self.user.username
        users_id = list(map(int, self.room_name.split("-")[1:]))
        for u_id in users_id:
            if u_id != self.user.pk:
                self.other_user = get_object_or_404(User, pk=u_id)
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        if self.user.pk in users_id:
            self.accept()

        # Send last massages
        last_messages = Message.get_last_messages(self.author, self.other_user.username)[::-1]
        for msg in last_messages:
            if msg.to == self.user.username:
                msg.readed = True
                msg.save()
            self.send(text_data=json.dumps({
                'message': msg.content,
                'message_author': msg.author + ": ",
            }))

        # Send info about user joining to chat
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
                {
                    'type': 'info_message',
                    'message': "{} dołączył do czatu.".format(self.author),
                    'author': "",
                }
        )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        msg = Message.objects.create(author=self.author, to=self.other_user, content=message)
        msg_id = msg.pk

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'author': self.author + ": ",
                'msg_id': msg_id,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        message_author = event['author']
        msg_id = event['msg_id']

        # Check if another user read message
        if self.user.username != message_author[:-2]:
            msg = get_object_or_404(Message, pk=msg_id)
            msg.readed = True
            msg.save()

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'message_author': message_author,
        }))

    # Get info messages
    def info_message(self, event):
        message = event['message']
        message_author = event['author']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'message_author': message_author,
        }))
