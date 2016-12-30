# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.response import Response
import logging
import requests
import docker
import time
from django.utils import timezone
from services.serializers import ServiceSerializer
from utils import service_DBclient
from django.shortcuts import render_to_response


# add.delay(2, 2)

def job_manage(request):
    print 'jinru le '
    print request
    if request.method == 'POST':
        render_to_response('job_manage.html', {'username': request.user.username})

    else:

        return render_to_response('job_manage.html', {'username': request.user.username})


def job_upload(request):
    if request.method == 'POST':
        render_to_response('job_upload.html', {'username': request.user.username})

    else:

        return render_to_response('job_upload.html', {'username': request.user.username})


def job_run(request):
    if request.method == 'POST':
        render_to_response('job_run.html', {'username': request.user.username})

    else:

        return render_to_response('job_run.html', {'username': request.user.username})
