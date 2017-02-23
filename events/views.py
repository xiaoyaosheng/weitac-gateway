# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
# from models import Service, Instance, Agent
import logging
import requests
import docker
# from docker import utils as docker_utils
import time
from django.utils import timezone
from services.serializers import ServiceSerializer
from utils import service_DBclient
from django.shortcuts import render_to_response
from jobs.views import call_agent_change_ip
from django.http import HttpRequest, QueryDict
from django.contrib.auth.decorators import login_required
from rest_framework.parsers import JSONParser, FormParser
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import permissions
import datetime
import base64
from django.http import HttpResponse
import json
import json
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.
def event_handle(request):
    instance_name = request.GET.get('instance_name')
    print request
    # if request.method == 'POST':
    #     ips = request.POST
    #     info_dic = {}
    return HttpResponse("success", status=status.HTTP_200_OK)
