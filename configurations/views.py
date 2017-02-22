# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from models import Configuration
from services.models import Agent
import logging

import ConfigParser
import StringIO
from utils.XML_client import del_xml_configuration
import requests
import docker
# from docker import utils as docker_utils
import time
from django.utils import timezone
from services.serializers import ServiceSerializer
from utils import service_DBclient
from django.shortcuts import render_to_response
from jobs.views import call_agent_cp_configuration
from services.models import Instance
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
logger = logging.getLogger(__name__)
from services.settings import SWARM_URL


def configuration_manage(request):
    if request.method == 'POST':
        # print request
        # delete_job(request)
        pass
    if request.method == 'PUT':
        # print request
        # delete_job(request)
        pass
    if request.method == 'DELETE':
        # print request
        # delete_job(request)
        pass

    scripts = Configuration.objects.all()
    # print scripts[0].job_name
    # , 'show_list': scripts
    return render_to_response(
        'configuration_manage.html', {
            'username': request.user.username, 'show_list': scripts})


def configuration_upload(request):
    if request.method == 'POST':
        # script= request.POST.get('script')
        # print type(script)
        print request
        myFile = request.FILES.get('script', None)
        name = request.POST.get('name')
        describe = request.POST.get('describe')
        print name, describe
        if name:
            save_name = name
        else:
            save_name = myFile
        # print(myFile._size)  # 文件大小字节数
        if Configuration.objects.filter(configuration_name=myFile).exists():
            return render_to_response('400.html', {'info': '脚本已经存在'})
        data = myFile.read()
        job_obj = Configuration()

        job_obj.configuration_name = save_name
        job_obj.info = data
        job_obj.describe = describe
        job_obj.save()
        return render_to_response(
            'configuration_upload.html', {
                'username': request.user.username})

    else:

        return render_to_response(
            'configuration_upload.html', {
                'username': request.user.username})


def configuration_update(request):
    if request.method == 'POST':
        # print request
        script_name = request.GET.get('job_name')

        if not script_name:
            return render_to_response('400.html')
        script_obj = Configuration.objects.filter(job_name=script_name)[0]
        agent_hosts_lis = request.POST.lists()

        # r = requests.post('http://10.6.168.161:8000', data=script, headers=headers)

        return render_to_response('configuration_manage.html')

    else:
        scripts = Configuration.objects.all()
        agents = Agent.objects.all()
        if not request.GET.get('job_name'):
            return render_to_response(
                'job_run.html', {
                    'username':
                        request.user.username, 'scripts': scripts,
                    'agents': agents})
        else:
            job_name = request.GET.get('job_name')
            return render_to_response(
                'job_run.html', {
                    'username':
                        request.user.username, 'scripts': scripts,
                    'agents': agents, 'choiced_script': job_name})


# class ServiceViewSet(viewsets.ModelViewSet):
#     model = Service
#     serializer_class = ServiceSerializer
#
#     permission_classes = (permissions.IsAuthenticated,)
#     #     authentication_classes = (SessionAuthentication, BasicAuthentication)
#     parser_classes = (JSONParser, FormParser)
#     @login_required
#
#     def create_service(self, request, **kwargs):
#         print 'jinle!!!!!'
#         if request.method == 'POST':
#             logger.info('Create a service: {}'.format(request.DATA))
#             print type(request.DATA)
#
#             if isinstance(request.DATA, QueryDict):
#                 data = {'service_name': request.DATA.get('service_name'),
#                         'instance_amount': request.DATA.get('instance_amount'),
#                         'image_name': 'ss', 'details': 'dd'}
#
#             elif isinstance(request.DATA, dict):
#                 data = request.DATA
#
#             serializer = ServiceSerializer(data=data)
#             if not serializer.is_valid():
#                 return Response(serializer.errors,
#                                 status=status.HTTP_400_BAD_REQUEST)
#             service = serializer.object
#             service_name = data['service_name']
#             instance_amount = data['instance_amount']
#             if not Service.objects.filter(service_name=service_name).exists():
#                 # serializer.save()
#                 db_info = dict()
#                 db_info['instance'] = []
#                 instance = Instance_client()
#                 for i in range(int(instance_amount)):
#                     # instance_name = service_name + '_{}'.format(i+1)
#                     instance_id = i + 1
#                     bl, result = instance.create_instance(service_name, instance_id)
#                     print bl
#                     if bl:
#                         instance.start_instance(result)
#                         db_info['instance'].append(bl)
#                         # return Response("success",
#                         #                 status=status.HTTP_200_OK)
#                     else:
#                         return Response('{}'.format(str(result)), status=status.HTTP_400_BAD_REQUEST)
#
#                 db_info['service'] = service
#                 service_DBclient.save(db_info)
#                 return render_to_response('create_service.html', {'username': request.user.username})
#
#             else:
#                 print 'Service {} exits'.format(service_name)
#                 return Response('Service {} exits. Do you want to add more instances? Please use update API'.format(
#                     data['service_name']), status=status.HTTP_400_BAD_REQUEST)
#         else:
#     return render_to_response('create_service.html', {'username':
#     request.user.username})


class ConfigurationViewSet(viewsets.ModelViewSet):
    def get_configuration(self, request, **kwargs):
        # if request.method == 'POST':
        #     # print request
        #     # delete_job(request)
        #     pass
        # if request.method == 'PUT':
        #     # print request
        #     # delete_job(request)
        #     pass
        # if request.method == 'DELETE':
        #     # print request
        #     # delete_job(request)
        #     pass
        # if request.method == 'GET':
        #     # print request
        #     # delete_job(request)
        #     pass
        pass

    def update_configuration(self, request):
        if request.method == 'PUT':
            data = request.DATA
            instance_name = data.get('instance_name')
            configuration_name = data.get('configuration_name')

            configuration_dir = data.get('configuration_dir')

            obj = Configuration.objects.get(configuration_name=configuration_name)
            file_obj = StringIO.StringIO()
            file_obj.write(obj.info)
            file_obj.seek(0)
            changed_file = StringIO.StringIO()
            configuration_type = configuration_name.split('.')[-1]
            if configuration_type == 'xml':

                change = data.get('change')
                new = data.get('new')

                config=del_xml_configuration(file_obj,change,new)

            elif configuration_type=='cnf':
                sections = data.get('parameters')
                config = ConfigParser.RawConfigParser(allow_no_value=True)
                s = StringIO.StringIO()

                s.write(obj.info)
                s.seek(0)
                config.readfp(s)

                for section, value_dic in sections.items():
                    # print section
                    for parameter, parameter_value in value_dic.items():
                        # print parameter, parameter_value

                        config.set(section, parameter, parameter_value)

            config.write(changed_file)
            changed_file.seek(0)
            # print changed_file.read()
            try:
                instance_obj = Instance.objects.get(name=instance_name)
            except Exception as ex:
                print ex
                return
            agent_obj = instance_obj.host
            # continer_ip_obj = instance_obj.continer_ip
            agent_host_ip = agent_obj.host_ip

            data = changed_file.read()
            dir = configuration_dir
            try:
                call_agent_cp_configuration(agent_host_ip, instance_name, configuration_name, data, dir)
            except Exception as ex:
                return Response(str(ex),
                                status=status.HTTP_400_BAD_REQUEST)

        return Response("success",
                        status=status.HTTP_200_OK)

    def upload_configuration(self, request):
        if request.GET.get('source') == 'master':
            data = request.DATA
            myFile = request.FILES.get('script', None)

            name = data.get('name')
            describe = data.get('describe')

            if name:
                save_name = name
            else:
                save_name = myFile.name
            # print(myFile._size)  # 文件大小字节数
            if Configuration.objects.filter(configuration_name=save_name).exists():
                return Response('脚本已经存在', status=status.HTTP_400_BAD_REQUEST)
            data = myFile.read()
            job_obj = Configuration()

            job_obj.configuration_name = save_name
            job_obj.info = data
            job_obj.describe = describe
            job_obj.save()
            return Response("success", status=status.HTTP_200_OK)

    def delete_configuration(self, reqest):
        pass
