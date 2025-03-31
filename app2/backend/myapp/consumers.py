import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class AvatarConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("WebSocket connected")

    async def disconnect(self, close_code):
        print("WebSocket disconnected")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(f"Received message: {message}")
        # You can process the message here if needed

    async def send_audio_command(self, event):
        """
        Sends a command to play or stop audio to the client.
        """
        message = event['message']
        await self.send(text_data=json.dumps(message))

def send_audio_command_to_client(action, value, script):
    """
    Sends a command to play or stop audio to the client.
    This function is called from outside the consumer.
    """
    channel_layer = get_channel_layer()
    message = {
        'action': action,
        'value': value,
        'script': script
    }
    async_to_sync(channel_layer.group_send)(
        "avatar_group",  # You can use a group name if you have multiple clients
        {
            'type': 'send_audio_command',
            'message': message
        }
    )
