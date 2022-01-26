from django.urls import path
from . import consumers

# Routes definite per le chiamate ai canali
# simile agli url di Django ma specifiche per i Channels

websocket_urlpatterns = [
    path('ws/partita<PartitaID>/', consumers.PartitaConsumer.as_asgi()),
]