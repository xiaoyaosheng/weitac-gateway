# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from models import Service, Instance, Agent, Image
import logging
import requests
import docker
# from docker import utils as docker_utils
import time
from django.utils import timezone
from services.serializers import ServiceSerializer
from utils import service_DBclient,instance_DBclient
from django.shortcuts import render_to_response
from jobs.views import call_agent_change_ip
from django.http import HttpRequest, QueryDict
from django.contrib.auth.decorators import login_required
from rest_framework.parsers import JSONParser, FormParser
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import permissions
import datetime
import base64
from django.http import HttpResponse, JsonResponse
import json
import json
from django.core.serializers.json import DjangoJSONEncoder
from settings import HARBOR_URL

logger = logging.getLogger(__name__)
from services.settings import SWARM_URL

swarm_client = docker.Client(base_url='tcp://{}'.format(SWARM_URL), timeout=60)


def datetime_to_timestamp(t):
    stamp = int(time.mktime(t.timetuple()))
    return stamp


def create_service(request, **kwargs):
    service_name = request.POST.get('service_name')
    instance_amount = request.POST.get('instance_amount')
    # ip= request.POST.get('ip')
    if not instance_amount:
        instance_amount = '1'
    image_name = request.POST.get('image_name')
    if not image_name:
        image_name = 'docker.weitac.com/centos7/haproxy:0.2'
    environment = request.POST.get('environment')
    if not environment:
        environment = None
    hostname = request.POST.get('hostname')
    if not hostname:
        environment = 'haproxy.weitac.com'
    command = request.POST.get('command')
    if not command:
        command = '/usr/sbin/init'
    volumes = request.POST.get('volumes')
    if not volumes:
        volumes = './conf:/etc/haproxy'
    if request.method == 'POST':
        logger.info('Create a service: {}'.format(service_name))

        data = {'service_name': service_name,
                'instance_amount': instance_amount,
                'image_name': image_name, 'details': 'dd'}
        # if isinstance(request.DATA, QueryDict):
        #     data = {'service_name': service_name,
        #             'instance_amount': instance_amount,
        #             'image_name': 'ss', 'details': 'dd'}
        #
        # elif isinstance(request.DATA, dict):
        #     data = request.DATA

        serializer = ServiceSerializer(data=data)
        if not serializer.is_valid():
            # return Response(serializer.errors,
            #                 status=status.HTTP_400_BAD_REQUEST)
            return render_to_response('400.html')
        service = serializer.object
        service_name = data['service_name']
        instance_amount = data['instance_amount']
        if not Service.objects.filter(service_name=service_name).exists():
            # serializer.save()
            db_info = dict()
            db_info['instance'] = []
            instance = Instance_client()
            for i in range(int(instance_amount)):
                # instance_name = service_name + '_{}'.format(i+1)
                instance_id = i + 1
                bl, result = instance.create_instance \
                    (service_name, instance_id, image_name, environment, hostname, command, volumes)
                if not bl:
                    return render_to_response('500.html')
                if bl:
                    instance.start_instance(result)
                    db_info['instance'].append(bl)
                    # return Response("success",
                    #                 status=status.HTTP_200_OK)
                else:
                    # return Response(
                    #     '{}'.format(
                    #         str(result)),
                    #     status=status.HTTP_400_BAD_REQUEST)
                    render_to_response('400.html')
            Instance_client().add_host_info(db_info)
            db_info['service'] = service
            service_DBclient.save(db_info)
            return render_to_response(
                'create_service.html', {
                    'username': request.user.username})

        else:
            logger.error('Service {} exits'.format(service_name))
            # return Response(
            #     'Service {} exits. Do you want to add more instances? Please use update API'.format(
            #         data['service_name']),
            #     status=status.HTTP_400_BAD_REQUEST)
            return render_to_response('400.html')
    else:
        return render_to_response(
            'create_service.html', {
                'username': request.user.username})

        #                                                        {'username':request.user.username,'ip_info':ip_info}


def get_services(request, **kwargs):
    if request.method == 'POST':
        delete_services(request)
    logger.info('Getting infomation was called')
    agent = request.GET.get('agent')
    detail = request.GET.get('detail')
    # if detail == 'true':
    #     result = swarm_client.containers()
    # else:
    #     result = []
    services = Service.objects.all()
    # for service in services:
    #     name = service.service_name
    #     instance_amount = service.instance_amount
    #     image_name = service.image_name
    #     updated_at = service.updated_at
    #     created_at = service.created_at
    #     service_dic = {'name': name, 'instance_amount': instance_amount,
    #                    'image_name': image_name, 'updated_at': updated_at,
    #                    'created_at': created_at}
    #     result.append(service_dic)
    return render_to_response(
        'service_manage.html', {
            'username': request.user.username, 'show_list': services})


def update_service(request):
    if request.method == "POST":
        service_name = request.POST.get('service_name')
        new_instance_amount = int(request.POST.get('instance_amount'))
        # data = request.DATA
        # logger.info('get user msg:{}'.format(data))
        # service_name = data.get('service_name')
        # new_instance_amount = int(data.get('instance_amount'))

        service_obj = Service.objects.filter(service_name=service_name)
        if not service_obj:
            # return Response(
            #     'Your service is not existed.',
            #     status=status.HTTP_400_BAD_REQUEST)
            return render_to_response('400.html')
        else:
            old_amount = service_obj[0].instance_amount
            change = new_instance_amount - old_amount
            logger.info('instance change{0}'.format(change))
            if change == 0:
                return render_to_response('400.html')
                # status=status.HTTP_400_BAD_REQUEST)
            if change > 0:
                logger.info('Start increase instances')
                for i in range(old_amount, new_instance_amount):
                    instance_obj = Instance.objects.get(service=service_obj[0])
                    print instance_obj
                    image_name = service_obj[0].image_name
                    environment = instance_obj.environment
                    hostname = instance_obj.hostname
                    command = instance_obj.command
                    volumes = instance_obj.volumes
                    bl, result = Instance_client(). \
                        create_instance(service_name, i + 1, image_name, environment,
                                        hostname, command, volumes)
                    if not bl:
                        return render_to_response('500.html')
                    bl.service = service_obj[0]
                    bl.save()
                    if not bl:
                        # return Response(
                        #     '{}'.format(
                        #         str(result)),
                        #     status=status.HTTP_400_BAD_REQUEST)
                        return render_to_response('400.html')
                    Instance_client().start_instance(result)
            if change < 0:
                logger.info('Start decrease instances')
                for i in range(new_instance_amount, old_amount):
                    logger.debug('{} start!'.format(i))
                    instance_name = service_name + '_{}'.format(i + 1)
                    ifSuccess = Instance_client().delete_instance(instance_name)
                    if not ifSuccess:
                        continue
                    Instance.objects.get(name=instance_name).delete()
                if new_instance_amount == 0:
                    service_obj.delete()
                    return render_to_response('update_service.html', {
                        'username': request.user.username})

        service_obj[0].instance_amount = new_instance_amount
        # service_obj[0].updated_at = datetime_to_timestamp(timezone.now())
        service_obj[0].updated_at = (timezone.now())
        service_obj[0].save()
        return render_to_response('update_service.html', {
            'username': request.user.username})
    else:
        return render_to_response('update_service.html', {
            'username': request.user.username})


def delete_services(request):
    post_services = request.POST.getlist('post_service')
    for post_service in post_services:
        service_name = post_service
        logger.debug('Start delete services :{}'.format(service_name))
        # print(('Start delete services :{}'.format(service_name)))
        try:
            service_obj = Service.objects.get(service_name=service_name)
        except Exception as ex:
            # return Response(
            #     'Service dose not exit. {}'.format(ex),
            #     status=status.HTTP_400_BAD_REQUEST)
            return render_to_response('400.html')

        instances = Instance.objects.filter(service=service_obj)
        for instance in instances:
            result = Instance_client().delete_instance(instance.continer_id)
            if result is True:
                instance.delete()
            else:
                # return Response(
                #     'Delete service error.',
                #     status=status.HTTP_400_BAD_REQUEST)
                return render_to_response('400.html')
        # if none
        service_obj.delete()
    # return Response('success', status=status.HTTP_200_OK)
    services = Service.objects.all()
    return render_to_response(
        'service_manage.html', {
            'username': request.user.username, 'show_list': services})


def instance_manage(request):
    service_name = request.GET.get('service_name')
    if request.method == 'POST':
        ips = request.POST
        info_dic = {}
        for info in ips:
            info_type = info.split('+')[-1]
            instance_name = info[:-len(info_type) - 1]
            if instance_name not in info_dic:
                info_dic[instance_name] = {}

            info_dic[instance_name][info_type] = ips[info]
        for instance_name in info_dic:
            instance_ip_info = info_dic[instance_name]
            ip = instance_ip_info.get('ip')
            subnet_mask = instance_ip_info.get('subnet_mask')
            gateway_ip = instance_ip_info.get('gateway_ip')

            # try:
            service_DBclient.change_db_ip(instance_name, ip, subnet_mask, gateway_ip)
            assignment_ip(instance_name)
            # except Exception as e:
            #     logger.error(e)

    service = Service.objects.get(service_name=service_name)
    instances = Instance.objects.filter(service=service)
    # for instance in instances:
    #     if not instance.continer_ip:
    #         continue
    # instance.ip=instance.continer_ip.address
    return render_to_response(
        'instance_manage.html', {
            'username': request.user.username, 'show_list': instances})


# def change_ip(instance_name, ip, subnet_mask, gateway_ip):
#     try:
#         call_agent_change_ip(agent_ip, instance_name, intance_ip, subnet_mask, gateway_ip)
#     except Exception as e:
#         logger.error(e)
#         return False
#     # print instance_name, ip
#     service_DBclient.change_db_ip(instance_name, ip, subnet_mask, gateway_ip)
#     return True


def assignment_ip(instance_name):
    try:
        instance_obj = Instance.objects.get(name=instance_name)
    except Exception as ex:
        logger.error('Did not have this instance {}:{}'.format(instance_name, ex))
        return
    if not instance_obj.continer_ip:
        return
    agent_ip = instance_obj.host.host_ip
    intance_ip = instance_obj.continer_ip.address
    subnet_mask = instance_obj.continer_ip.subnet_mask
    gateway_ip = instance_obj.continer_ip.gateway_ip
    call_agent_change_ip.delay(agent_ip, instance_name, intance_ip, subnet_mask, gateway_ip)


class ServiceViewSet(viewsets.ModelViewSet):
    model = Service
    serializer_class = ServiceSerializer

    # permission_classes = (permissions.IsAuthenticated,)
    #     authentication_classes = (SessionAuthentication, BasicAuthentication)
    # parser_classes = (JSONParser, FormParser)
    # @login_required
    def create_service(self, request, **kwargs):
        if request.GET.get('source') == 'master':
            service_name = request.DATA.get('service_name')
            instance_amount = request.DATA.get('instance_amount')
            # ip= request.DATA.get('ip')
            if not instance_amount:
                instance_amount = '1'
            image_name = request.DATA.get('image_name')
            if not image_name:
                image_name = 'docker.weitac.com/centos7/haproxy:0.2'
            environment = request.DATA.get('environment')
            if not environment:
                environment = None
            hostname = request.DATA.get('hostname')
            if not hostname:
                environment = 'haproxy.weitac.com'
            command = request.DATA.get('command')
            if not command:
                command = '/usr/sbin/init'
            volumes = request.DATA.get('volumes')
            if not volumes:
                # volumes = './conf:/etc/haproxy'
                volumes = None
            if request.method == 'POST':
                logger.info('Create a service: {}'.format(service_name))

                data = {'service_name': service_name,
                        'instance_amount': instance_amount,
                        'image_name': image_name, 'details': 'dd'}
                # if isinstance(request.DATA, QueryDict):
                #     data = {'service_name': service_name,
                #             'instance_amount': instance_amount,
                #             'image_name': 'ss', 'details': 'dd'}
                #
                # elif isinstance(request.DATA, dict):
                #     data = request.DATA

                serializer = ServiceSerializer(data=data)
                if not serializer.is_valid():
                    return Response(serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
                    # return render_to_response('400.html')
                service = serializer.object
                service_name = data['service_name']
                instance_amount = data['instance_amount']
                if not Service.objects.filter(service_name=service_name).exists():
                    # serializer.save()
                    db_info = dict()
                    db_info['instance'] = []
                    instance = Instance_client()
                    for i in range(int(instance_amount)):
                        # instance_name = service_name + '_{}'.format(i+1)
                        instance_id = i + 1
                        bl, result = instance.create_instance \
                            (service_name, instance_id, image_name, environment, hostname, command, volumes)
                        if not bl:
                            # return render_to_response('500.html')
                            return Response('Fault',
                                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        if bl:
                            instance.start_instance(result)
                            db_info['instance'].append(bl)
                            # return Response("success",
                            #                 status=status.HTTP_200_OK)
                        else:
                            # return Response(
                            #     '{}'.format(
                            #         str(result)),
                            #     status=status.HTTP_400_BAD_REQUEST)
                            render_to_response('400.html')
                    Instance_client().add_host_info(db_info)
                    db_info['service'] = service
                    service_DBclient.save(db_info)
                    return Response("success", status=status.HTTP_200_OK)

                else:
                    logger.error('Service {} exits'.format(service_name))
                    return Response(
                        'Service {} exits. Do you want to add more instances? Please use update API'.format(
                            data['service_name']),
                        status=status.HTTP_400_BAD_REQUEST)
                    # return render_to_response('400.html')
            else:
                return Response("success", status=status.HTTP_200_OK)
        else:
            """
            前端的进入，返回页面
            """
            service_name = request.DATA.get('service_name')
            instance_amount = request.DATA.get('instance_amount')
            # ip= request.DATA.get('ip')
            if not instance_amount:
                instance_amount = '1'
            image_name = request.DATA.get('image_name')
            if not image_name:
                image_name = 'docker.weitac.com/centos7/haproxy:0.2'
            environment = request.DATA.get('environment')
            if not environment:
                environment = None
            hostname = request.DATA.get('hostname')
            if not hostname:
                environment = 'haproxy.weitac.com'
            command = request.DATA.get('command')
            if not command:
                command = '/usr/sbin/init'
            volumes = request.DATA.get('volumes')
            if not volumes:
                volumes = './conf:/etc/haproxy'
            if request.method == 'POST':
                logger.info('Create a service: {}'.format(service_name))

                data = {'service_name': service_name,
                        'instance_amount': instance_amount,
                        'image_name': image_name, 'details': 'dd'}
                # if isinstance(request.DATA, QueryDict):
                #     data = {'service_name': service_name,
                #             'instance_amount': instance_amount,
                #             'image_name': 'ss', 'details': 'dd'}
                #
                # elif isinstance(request.DATA, dict):
                #     data = request.DATA

                serializer = ServiceSerializer(data=data)
                if not serializer.is_valid():
                    # return Response(serializer.errors,
                    #                 status=status.HTTP_400_BAD_REQUEST)
                    return render_to_response('400.html')
                service = serializer.object
                service_name = data['service_name']
                instance_amount = data['instance_amount']
                if not Service.objects.filter(service_name=service_name).exists():
                    # serializer.save()
                    db_info = dict()
                    db_info['instance'] = []
                    instance = Instance_client()
                    for i in range(int(instance_amount)):
                        # instance_name = service_name + '_{}'.format(i+1)
                        instance_id = i + 1
                        bl, result = instance.create_instance \
                            (service_name, instance_id, image_name, environment, hostname, command, volumes)
                        if not bl:
                            return render_to_response('500.html')
                        if bl:
                            instance.start_instance(result)
                            db_info['instance'].append(bl)
                            # return Response("success",
                            #                 status=status.HTTP_200_OK)
                        else:
                            # return Response(
                            #     '{}'.format(
                            #         str(result)),
                            #     status=status.HTTP_400_BAD_REQUEST)
                            render_to_response('400.html')
                    Instance_client().add_host_info(db_info)
                    db_info['service'] = service
                    service_DBclient.save(db_info)
                    return render_to_response(
                        'create_service.html', {
                            'username': request.user.username})

                else:
                    logger.error('Service {} exits'.format(service_name))
                    # return Response(
                    #     'Service {} exits. Do you want to add more instances? Please use update API'.format(
                    #         data['service_name']),
                    #     status=status.HTTP_400_BAD_REQUEST)
                    return render_to_response('400.html')
            else:
                return render_to_response(
                    'create_service.html', {
                        'username': request.user.username})

    def delete_services(self, request):
        if request.GET.get('source') == 'master':
            print request.DATA
            service_name = request.DATA.get('service_name')
            # for post_service in post_services:
            # service_name = post_service
            logger.debug('Start delete services :{}'.format(service_name))
            # print(('Start delete services :{}'.format(service_name)))
            try:
                service_obj = Service.objects.get(service_name=service_name)
            except Exception as ex:
                return Response(
                    'Service dose not exit. {}'.format(ex),
                    status=status.HTTP_400_BAD_REQUEST)
                # return render_to_response('400.html')

            instances = Instance.objects.filter(service=service_obj)
            for instance in instances:
                result = Instance_client().delete_instance(instance.continer_id)
                if result is True:
                    instance.delete()
                else:
                    return Response(
                        'Delete service error.',
                        status=status.HTTP_400_BAD_REQUEST)
                    # return render_to_response('400.html')
            # if none
            service_obj.delete()
            # return Response('success', status=status.HTTP_200_OK)
            # services = Service.objects.all()
            # return render_to_response(
            #     'service_manage.html', {
            #         'username': request.user.username, 'show_list': services})
            return Response('success', status=status.HTTP_200_OK)
        else:
            post_services = request.DATA.getlist('post_service')
            for post_service in post_services:
                service_name = post_service
                logger.debug('Start delete services :{}'.format(service_name))
                # print(('Start delete services :{}'.format(service_name)))
                try:
                    service_obj = Service.objects.get(service_name=service_name)
                except Exception as ex:
                    # return Response(
                    #     'Service dose not exit. {}'.format(ex),
                    #     status=status.HTTP_400_BAD_REQUEST)
                    return render_to_response('400.html')

                instances = Instance.objects.filter(service=service_obj)
                for instance in instances:
                    result = Instance_client().delete_instance(instance.continer_id)
                    if result is True:
                        instance.delete()
                    else:
                        # return Response(
                        #     'Delete service error.',
                        #     status=status.HTTP_400_BAD_REQUEST)
                        return render_to_response('400.html')
                # if none
                service_obj.delete()
            # return Response('success', status=status.HTTP_200_OK)
            services = Service.objects.all()
            return render_to_response(
                'service_manage.html', {
                    'username': request.user.username, 'show_list': services})

    def update_services(self, request):
        if request.GET.get('source') == 'master':
            # service_name = request.POST.get('service_name')
            # new_instance_amount = int(request.POST.get('instance_amount'))
            data = request.DATA
            logger.info('get user msg:{}'.format(data))
            service_name = data.get('service_name')
            new_instance_amount = int(data.get('instance_amount'))

            service_obj = Service.objects.filter(service_name=service_name)
            if not service_obj:
                return Response(
                    'Your service is not existed.',
                    status=status.HTTP_400_BAD_REQUEST)
                # return render_to_response('400.html')
            else:
                old_amount = service_obj[0].instance_amount
                change = new_instance_amount - old_amount
                logger.info('instance change{0}'.format(change))
                if change == 0:
                    # return render_to_response('400.html')
                    return Response("no change", status=status.HTTP_200_OK)
                if change > 0:
                    logger.info('Start increase instances')
                    for i in range(old_amount, new_instance_amount):
                        instance_obj = Instance.objects.get(service=service_obj[0])
                        print instance_obj
                        image_name = service_obj[0].image_name
                        environment = instance_obj.environment
                        hostname = instance_obj.hostname
                        command = instance_obj.command
                        volumes = instance_obj.volumes
                        bl, result = Instance_client(). \
                            create_instance(service_name, i + 1, image_name, environment,
                                            hostname, command, volumes)
                        if not bl:
                            # return render_to_response('500.html')
                            return Response('False', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                        bl.service = service_obj[0]
                        bl.save()
                        if not bl:
                            return Response(
                                '{}'.format(
                                    str(result)),
                                status=status.HTTP_400_BAD_REQUEST)
                            # return render_to_response('400.html')
                        Instance_client().start_instance(result)
                if change < 0:
                    logger.info('Start decrease instances')
                    for i in range(new_instance_amount, old_amount):
                        logger.debug('{} start!'.format(i))
                        instance_name = service_name + '_{}'.format(i + 1)
                        ifSuccess = Instance_client().delete_instance(instance_name)
                        if not ifSuccess:
                            continue
                        Instance.objects.get(name=instance_name).delete()
                    if new_instance_amount == 0:
                        service_obj.delete()
                        # return render_to_response('update_service.html', {
                        #     'username': request.user.username})
                        return Response("deleted success", status=status.HTTP_200_OK)
            service_obj[0].instance_amount = new_instance_amount
            # service_obj[0].updated_at = datetime_to_timestamp(timezone.now())
            service_obj[0].updated_at = (timezone.now())
            service_obj[0].save()
            # return render_to_response('update_service.html', {
            #     'username': request.user.username})
            return Response("success", status=status.HTTP_200_OK)
        else:
            # service_name = request.POST.get('service_name')
            # new_instance_amount = int(request.POST.get('instance_amount'))
            data = request.DATA
            logger.info('get user msg:{}'.format(data))
            service_name = data.get('service_name')
            new_instance_amount = int(data.get('instance_amount'))

            service_obj = Service.objects.filter(service_name=service_name)
            if not service_obj:
                # return Response(
                #     'Your service is not existed.',
                #     status=status.HTTP_400_BAD_REQUEST)
                return render_to_response('400.html')
            else:
                old_amount = service_obj[0].instance_amount
                change = new_instance_amount - old_amount
                logger.info('instance change{0}'.format(change))
                if change == 0:
                    return render_to_response('400.html')
                    # status=status.HTTP_400_BAD_REQUEST)
                if change > 0:
                    logger.info('Start increase instances')
                    for i in range(old_amount, new_instance_amount):
                        instance_obj = Instance.objects.get(service=service_obj[0])
                        print instance_obj
                        image_name = service_obj[0].image_name
                        environment = instance_obj.environment
                        hostname = instance_obj.hostname
                        command = instance_obj.command
                        volumes = instance_obj.volumes
                        bl, result = Instance_client(). \
                            create_instance(service_name, i + 1, image_name, environment,
                                            hostname, command, volumes)
                        if not bl:
                            return render_to_response('500.html')
                        bl.service = service_obj[0]
                        bl.save()
                        if not bl:
                            # return Response(
                            #     '{}'.format(
                            #         str(result)),
                            #     status=status.HTTP_400_BAD_REQUEST)
                            return render_to_response('400.html')
                        Instance_client().start_instance(result)
                if change < 0:
                    logger.info('Start decrease instances')
                    for i in range(new_instance_amount, old_amount):
                        logger.debug('{} start!'.format(i))
                        instance_name = service_name + '_{}'.format(i + 1)
                        ifSuccess = Instance_client().delete_instance(instance_name)
                        if not ifSuccess:
                            continue
                        Instance.objects.get(name=instance_name).delete()
                    if new_instance_amount == 0:
                        service_obj.delete()
                        return render_to_response('update_service.html', {
                            'username': request.user.username})

            service_obj[0].instance_amount = new_instance_amount
            # service_obj[0].updated_at = datetime_to_timestamp(timezone.now())
            service_obj[0].updated_at = (timezone.now())
            service_obj[0].save()
            return render_to_response('update_service.html', {
                'username': request.user.username})

    def get_services(self, request, **kwargs):
        if request.GET.get('source') == 'master':
            logger.info('Getting infomation was called')
            agent = request.GET.get('agent')
            detail = request.GET.get('detail')
            services = Service.objects.all()
            # for service in services:
            # return render_to_response(
            #     'service_manage.html', {
            #         'username': request.user.username, 'show_list': services})

            return Response(ServiceSerializer(services).data, status=status.HTTP_200_OK)
        else:
            logger.info('Getting infomation was called')
            agent = request.GET.get('agent')
            detail = request.GET.get('detail')
            services = Service.objects.all()
            # for service in services:
            return render_to_response(
                'service_manage.html', {
                    'username': request.user.username, 'show_list': services})


class Instance_client(object):
    model = Instance

    def create_instance(self, service_name, instance_id, image_name, environment, hostname, command, volumes):
        instance_name = service_name + '_{}'.format(instance_id)

        logger.info('Create a docker instance: {}'.format(instance_name))
        # cmd_data = ["nginx",
        #             "-g",
        #             "daemon off;"]
        # labels_data = {
        #     "com.example.vendor": "Acme",
        #     "com.example.license": "GPL",
        #     "com.example.version": "1.0"}
        # HostConfig = {"NetworkMode": "bridge"}
        try:
            print image_name, command, instance_name, hostname, volumes
            r = swarm_client.create_container(image=image_name,
                                              command=command,
                                              name=instance_name,
                                              # environment=environment,
                                              hostname=hostname,
                                              volumes=volumes,

                                              )

        except Exception as ex:
            logger.error("Error{}".format(ex))
            return None, ex
        # service = Service.objects.get(service_name=service_name)
        container_id = r.get('Id')
        # created_at = datetime_to_timestamp(timezone.now())
        created_at = (timezone.now())
        try:
            """
            create agent info in db.
            """
            a = swarm_client.inspect_container(container_id)

            node_name = a.get('Node').get('Name')
            node_ip = a.get('Node').get('IP')
            agent_obj = service_DBclient.create_agent_info(node_name, node_ip)
        except Exception as ex:
            agent_obj = None
            logger.debug('Did not get agent info:{}'.format(ex))
        b = Instance(name=instance_name, created_at=created_at,
                     instance_id=instance_id,
                     continer_id=container_id,
                     command=command,
                     hostname=hostname,
                     volumes=volumes,
                     environment=environment,
                     host=agent_obj
                     )
        # service = service,
        # host='hostname'
        # b.save()
        # container_id = json.loads(r.text).get('Id')
        logger.info('Create docker continer :{}'.format(instance_name))
        return b, container_id

    def start_instance(self, continer_id):
        logger.info('Start continer of: {}'.format(continer_id))

        try:
            swarm_client.start(container=continer_id)
            # requests.post(SWARM_URL + '/containers/{}/start'.format(continer_id))
        except Exception as ex:
            logger.error("Error: {}".format(ex))

    def delete_instance(self, continer_id):
        logger.info('Delete continer of: {}'.format(continer_id))
        # print continer_id
        try:
            swarm_client.stop(container=continer_id)
            swarm_client.remove_container(container=continer_id)
        except requests.exceptions.HTTPError as ex:
            logger.error("Error: {}".format(ex))
            return True
        except requests.exceptions.ConnectionError as ex:
            logger.error("Error: {}".format(ex))
            return False
        return True

    def add_host_info(self, db_info):
        mapping = {}
        a = swarm_client.containers()
        for b in a:
            host_name = b.get('Names')[0].split('/')[1]
            server_name = b.get('Names')[0].split('/')[2]
            mapping[server_name] = host_name
        instances = db_info.get('instance')
        for instance in instances:
            host_name = mapping.get(instance.name)
            try:
                instance.host = Agent.objects.get(host_name=host_name)
            except:
                pass
        return db_info

    def stop_instance(self, instance_name):
        logger.info('Stop continer of: {}'.format(instance_name))

        try:
            swarm_client.stop(container=instance_name)

            return True
            # requests.post(SWARM_URL + '/containers/{}/start'.format(continer_id))
        except Exception as ex:
            logger.error("Error: {}".format(ex))
            return False

    def get_exited_instance(self):
        result_list=[]
        exited_containers = swarm_client.containers(filters={'status': 'exited'})
        for exited_container in exited_containers:
            container= exited_container['Names'][0].split('/')[-1]
            result_list.append(container)
        return result_list

class ImageViewSet(viewsets.ModelViewSet):
    def update_image(self, request, **kwargs):

        request_json = False
        if 'json' in request.GET.keys():
            request_json = True
        try:
            r = requests.get('{}/api/search'.format(HARBOR_URL))
        except requests.ConnectionError as ex:
            logger.error(ex)
            return Response('Fail connet to Harbor.try again', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as ex:
            logger.error(ex)
            return Response('Fail', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # http://10.6.168.54/api/repositories/tags?repo_name=tengyu/weitac_gateway
        dic_info = json.loads(r.text)
        repositorys = dic_info.get('repository')
        for repository in repositorys:
            repository_name = repository.get('repository_name')
            tags_str = requests.get('{0}/api/repositories/tags?repo_name={1}'.format(HARBOR_URL, repository_name))
            tags = json.loads(tags_str.text)

            for tag in tags:
                project = repository_name.split('/')[0]
                repository = repository_name.split('/')[1]
                create_update_image(project, repository, tag)
        if request_json == True:
            return Response('Update success', status=status.HTTP_200_OK)
        else:
            return HttpResponse('Update success', status=status.HTTP_200_OK)

    def get_image(self, request, **kwargs):
        request_json = False
        if 'json' in request.GET.keys():
            request_json = True

        result = dict()
        images = Image.objects.all()
        for image in images:
            if image.project not in result:
                result.setdefault(image.project)
                result[image.project] = dict()
            if image.repository not in result[image.project]:
                result[image.project].setdefault(image.repository)
                result[image.project][image.repository] = list()
            result[image.project][image.repository].append(image.tag)
        if request_json == True:
            return Response(result, status=status.HTTP_200_OK)
        else:
            return HttpResponse(result, status=status.HTTP_200_OK)


def create_update_image(project, repository, tag):
    if not Image.objects.filter(project=project, repository=repository, tag=tag):
        logger.info('add new {}/{}:{}'.format(project, repository, tag))
        image_obj = Image()
        image_obj.project = project
        image_obj.repository = repository
        image_obj.tag = tag
        image_obj.name = 'docker.weitac.com/{}/{}:{}'.format(project, repository, tag)
        image_obj.save()


class InstanceViewSet(viewsets.ModelViewSet):
    def stop_instance(self, request):
        data = request.DATA
        print data
        instances = data.get('instance')

        for instance in instances:
            result=Instance_client().stop_instance(instance)

            if result is True:
                if instance in Instance_client().get_exited_instance():
                    instance_DBclient.update_instance(instance,status='Exited')
            else:
                # return Response(
                #     'Delete service error.',
                #     status=status.HTTP_400_BAD_REQUEST)
                return render_to_response('400.html')
        # if none

        # return Response('success', status=status.HTTP_200_OK)
        services = Service.objects.all()
        return render_to_response(
            'service_manage.html', {
                'username': request.user.username, 'show_list': services})

    def create_instance(self):
        pass
    def delete_instance(self):
        pass
    def get_instances(self):
        pass