import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from main.models import Message
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncJsonWebsocketConsumer):
    @sync_to_async
    def check_user(self, user, conv_id):
        conversations = user.conversations.all()
        if int(conv_id) in [x.id for x in list(conversations)]:
            return True
        return False

    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['id']
        self.conversation_name = f'room_{self.conversation_id}'

        if not await self.check_user(self.scope["user"], self.conversation_id):
            await self.close()

        # Join room group
        await self.channel_layer.group_add(
            self.conversation_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")
        # Leave room group
        await self.channel_layer.group_discard(
            self.conversation_name,
            self.channel_name
        )

    @sync_to_async
    def add_msg_to_conv(self, msg):
        msg.save()
        msg.read_by.add(self.scope["user"])
        c = self.scope["user"].conversations.get(pk=int(self.conversation_id))
        c.messages.add(msg)
        c.last_message = msg
        c.save()

    @sync_to_async
    def delete_message(self, msg_id):
        m = Message.objects.get(pk=msg_id)

        if m.author == self.scope["user"]:
            if hasattr(m, "last_message_conversation"):
                c = m.last_message_conversation
                messages_list = c.messages.all().order_by('-date_sent')
                if len(messages_list) > 1:
                    new_last_message = messages_list[1]
                else:
                    new_last_message = None
                c.last_message = new_last_message
                c.save()
            m.delete()
        else:
            print("[-] Unauthorized attempt to delete a message")

    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        # try:
        response = json.loads(text_data)
        action = response.get("action", None)
        message = response.get("message", None)
        if action == 'SEND':
            token = response.get("token", None)
            # Save message to db
            m = Message()
            m.author = self.scope["user"]
            m.text = message
            await self.add_msg_to_conv(m)

            data = {
                "text": message,
                "id": m.id,
                "author": self.scope["user"].username,
                "token": token
            }

            # Send message to room group
            await self.channel_layer.group_send(self.conversation_name, {
                'type': "send_message",
                'message': json.dumps(data),
                "action": "SEND"
            })
        elif action == 'DELETE':
            msg_id = message

            await self.delete_message(msg_id)

            data = {
                "id": msg_id
            }

            # Send message to room group
            await self.channel_layer.group_send(self.conversation_name, {
                'type': "send_message",
                'message': json.dumps(data),
                'action': "DELETE"
            })
        # except Exception:
        #     pass

    @sync_to_async
    def mark_read(self, msg_id):
        msg = Message.objects.get(pk=int(msg_id))
        msg.read_by.add(self.scope["user"])

    async def send_message(self, res):
        """ Receive message from room group """
        data = json.loads(res["message"])

        if res["action"] == "SEND":
            await self.mark_read(data["id"])

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res,
        }))


class GroupChatConsumer(AsyncJsonWebsocketConsumer):
    @sync_to_async
    def check_user(self, user, group_id):
        groups = user.group_set.all()
        if int(group_id) in [x.id for x in list(groups)]:
            return True
        return False

    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['id']
        self.group_name = f'group_{self.group_id}'

        if not await self.check_user(self.scope["user"], self.group_id):
            await self.close()

        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print("Disconnected")
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    @sync_to_async
    def add_msg_to_group(self, msg):
        msg.save()
        msg.read_by.add(self.scope["user"])
        g = self.scope["user"].group_set.get(pk=int(self.group_id))
        g.messages.add(msg)
        g.last_message = msg
        g.save()

    @sync_to_async
    def delete_message(self, msg_id):
        m = Message.objects.get(pk=msg_id)

        if m.author == self.scope["user"]:
            if hasattr(m, "last_message_group"):
                g = m.last_message_group
                messages_list = g.messages.all().order_by('-date_sent')
                if len(messages_list) > 1:
                    new_last_message = messages_list[1]
                else:
                    new_last_message = None
                g.last_message = new_last_message
                g.save()
            m.delete()
        else:
            print("[-] Unauthorized attempt to delete a message")

    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Get the event and send the appropriate event
        """
        # try:
        response = json.loads(text_data)
        action = response.get("action", None)
        message = response.get("message", None)
        if action == 'SEND':
            token = response.get("token", None)
            # Save message to db
            m = Message()
            m.author = self.scope["user"]
            m.text = message
            await self.add_msg_to_group(m)

            data = {
                "text": message,
                "id": m.id,
                "author": self.scope["user"].username,
                "token": token
            }

            # Send message to room group
            await self.channel_layer.group_send(self.group_name, {
                'type': "send_message",
                'message': json.dumps(data),
                "action": "SEND"
            })
        elif action == 'DELETE':
            msg_id = message

            await self.delete_message(msg_id)

            data = {
                "id": msg_id
            }

            # Send message to room group
            await self.channel_layer.group_send(self.group_name, {
                'type': "send_message",
                'message': json.dumps(data),
                'action': "DELETE"
            })
        # except Exception:
        #     pass

    @sync_to_async
    def mark_read(self, msg_id):
        msg = Message.objects.get(pk=int(msg_id))
        msg.read_by.add(self.scope["user"])

    async def send_message(self, res):
        """ Receive message from room group """
        data = json.loads(res["message"])

        if res["action"] == "SEND":
            await self.mark_read(data["id"])

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res,
        }))
