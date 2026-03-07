import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Booking, Message
from django.utils.timezone import localtime

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.booking_id = self.scope['url_route']['kwargs']['booking_id']
        self.room_group_name = f'chat_{self.booking_id}'

        # Check authentication
        if self.scope["user"].is_anonymous:
            await self.close()
            return

        # Verify user is part of the booking
        is_participant = await self.is_booking_participant(self.booking_id, self.scope["user"])
        if not is_participant:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_id = self.scope["user"].id

        # Save message to database
        new_msg = await self.save_message(self.booking_id, sender_id, message)
        
        # Convert UTC to Local time matching template 'h:i A' format
        local_time = localtime(new_msg.timestamp)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.scope["user"].username,
                'timestamp': local_time.strftime("%I:%M %p")
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        timestamp = event.get('timestamp', '')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp': timestamp
        }))

    @database_sync_to_async
    def is_booking_participant(self, booking_id, user):
        try:
            booking = Booking.objects.get(id=booking_id)
            return user == booking.user or user == booking.service_provider.user
        except Booking.DoesNotExist:
            return False

    @database_sync_to_async
    def save_message(self, booking_id, sender_id, message):
        booking = Booking.objects.get(id=booking_id)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        sender = User.objects.get(id=sender_id)
        return Message.objects.create(booking=booking, sender=sender, content=message)
