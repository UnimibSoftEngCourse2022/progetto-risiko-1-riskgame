import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class PartitaConsumer(WebsocketConsumer):
 
    # Set to True to automatically port users from HTTP cookies
    # (you don't need channel_session_user, this implies it)
    http_user = True 

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['PartitaID']
        self.room_group_name = 'partita_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

 
    def receive(self, text_data):
        # Chiamato alla ricezione di un messaggio (testo o bytes)
        text_data_json = json.loads(text_data)
        print(text_data_json)
        tipo = text_data_json['tipo']
        mittente = self.scope['user'].username

        # Metti messaggio in room group (locale)
        if (tipo == 'messaggio'):
            messaggio = text_data_json['message']
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'tipo': 'messaggio',
                    'message': messaggio,
                    'sender': mittente
                }
            )
        elif (tipo == 'nuovoGiocatore'):
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'tipo': 'nuovoGiocatore',
                    'sender': mittente
                }
            )


    # Riceve il messaggio dalla room group (locale)
    def chat_message(self, event):
        tipo = event['tipo']

        # Invia esternamente alla WebSocket
        if (tipo == 'messaggio'):
            messaggio = event['message']
            self.send(text_data=json.dumps({
                'tipo': tipo,
                'message': messaggio,
                'sender': event['sender']
            }))
        elif (tipo == 'nuovoGiocatore'):
            self.send(text_data=json.dumps({
                'tipo': tipo,
                'sender': event['sender']
            }))
