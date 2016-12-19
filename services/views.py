from django.shortcuts import render
from rest_framework import viewsets
from models import Service
# Create your views here.


class ServiceViewSet(viewsets.ModelViewSet):
    model = Service
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticated,)
#     authentication_classes = (SessionAuthentication, BasicAuthentication)
    parser_classes = (JSONParser, FormParser)

    def event_listener(self, request, **kwargs):
        logger.info('Recieve an event: {}'.format(request.DATA))
