from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.
class EventViewSet(viewsets.ModelViewSet):
    model = Event
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticated,)
#     authentication_classes = (SessionAuthentication, BasicAuthentication)
    parser_classes = (JSONParser, FormParser)

    def event_listener(self, request, **kwargs):
        logger.info('Recieve an event: {}'.format(request.DATA))
