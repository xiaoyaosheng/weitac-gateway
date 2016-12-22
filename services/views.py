from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import viewsets
from models import Service, Instance
from services.serializers import ServiceSerializer
from rest_framework import permissions
import datetime
import logging
import requests
import base64
from django.db.models import Q
from django.http import HttpResponse
import docker

logger = logging.getLogger(__name__)
import json
from services.settings import SWARM_URL
from services.serializers import ServiceSerializer
import time
from django.utils import timezone

swarm_client = docker.Client(base_url='tcp://10.6.168.160:2376', timeout=10)


def datetime_to_timestamp(t):
    stamp = int(time.mktime(t.timetuple()))
    return stamp


class ServiceViewSet(viewsets.ModelViewSet):
    model = Service
    serializer_class = ServiceSerializer

    #     permission_classes = (permissions.IsAuthenticated,)
    # #     authentication_classes = (SessionAuthentication, BasicAuthentication)
    #     parser_classes = (JSONParser, FormParser)

    def create_services(self, request, **kwargs):
        logger.info('Create a service: {}'.format(request.DATA))
        data = request.DATA
        serializer = ServiceSerializer(data=request.DATA)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        # service = serializer.create()

        # try:
        service_name = data['service_name']
        instance_amount = data['instance_amount']

        if not Service.objects.filter(service_name=service_name).exists():
            serializer.save()
            instance = Instance_client()
            for i in range(int(instance_amount)):
                # instance_name = service_name + '_{}'.format(i+1)
                instance_id = i+1
                container_id=instance.create_instance(service_name,instance_id)
                instance.start_continer(container_id)
                # print 'created docker\' continer_id is Null'
                # return Response('Service Error', status=status.HTTP_400_BAD_REQUEST)
        else:
            print 'Service {} exits'.format(service_name)
            return Response('Service {} exits. Do you want to add more instances? Please use update API'.format(
                data['service_name']), status=status.HTTP_400_BAD_REQUEST)

        created_at = datetime_to_timestamp(timezone.now())
        service_obj = Service.objects.get(service_name=service_name)
        service_obj.created_at = created_at
        service_obj.save()
        return Response('success', status=status.HTTP_200_OK)
        # logging.debug('object after serialized: {}'.format(service))

    def delete_services(self, request):
        data = request.DATA
        service_name = data.get('service_name')
        logger.debug('Start delete services :{}'.format(service_name))

        try:
            service_obj=Service.objects.get(service_name=service_name)
        except Exception as ex:
            return Response('Service dose not exit. {}'.format(ex), status=status.HTTP_400_BAD_REQUEST)

        instances=Instance.objects.filter(service=service_obj)
        for instance in instances:
            result=Instance_client().delete_instance(instance.continer_id)
            if result is True:
                instance.delete()
            else:
                return Response('Delete service error.', status=status.HTTP_400_BAD_REQUEST)
        # if none
        service_obj.delete()
        return Response('success', status=status.HTTP_200_OK)


    def update_services(self, request):
        data = request.DATA
        logger.info('get user msg:{}'.format(data))
        service_name=data.get('service_name')
        new_instance_amount=int(data.get('instance_amount'))

        service_obj=Service.objects.filter(service_name=service_name)
        if not service_obj:
            return Response('Your service is not existed.', status=status.HTTP_400_BAD_REQUEST)
        else:
            old_amount=service_obj[0].instance_amount
            change=new_instance_amount-old_amount
            print change
            if change==0:
                return Response('The instance_amount is already {}.'.format(new_instance_amount), status=status.HTTP_400_BAD_REQUEST)
            if change>0:
                for i in range(old_amount,new_instance_amount):
                    result,ex=Instance_client().create_instance(service_name,i+1)
                    if not result:
                        return Response('{}'.format(str(ex)), status=status.HTTP_400_BAD_REQUEST)
            if change<0:
                print 'yes'
                for i in range(new_instance_amount,old_amount):
                    instance_name=service_name+'_{}'.format(i+1)
                    Instance_client().delete_instance(instance_name)
                    Instance.objects.get(name=instance_name).delete()
                    if i==0:
                        service_obj.delete()

        return Response("success",
                        status=status.HTTP_200_OK)



    # def get_services(self, request, **kwargs):
    #     logger.info('trigger was called!')
    #     if not settings.TRIGGER:
    #         return Response("trigger is false!",
    #                         status=status.HTTP_200_OK)
    #     rows = MultiCloudInfo.objects.all()
    #     logger.info('multicloudinfo len:{}'.format(len(rows)))
    #     if len(rows) == 0:
    #         marathon_url = settings.CLUSTER_SCHEDULER['endpoint']
    #         result = [{'url': marathon_url, 'username': "", 'password': ""}]
    #     else:
    #         result = []
    #         for cloud in rows:
    #             result.append(cloud.marathon_settings)
    #
    #     return Response(result, status=status.HTTP_200_OK)










class Instance_client(object):
    model = Instance

    def create_instance(self, service_name,instance_id):
        instance_name = service_name + '_{}'.format(instance_id)
        service = Service.objects.get(service_name=service_name)
        logger.info('Create a docker instance: {}'.format(instance_name))
        cmd_data = ["nginx",
                    "-g",
                    "daemon off;"]
        image_data = "nginx"
        env_data = ["FOO=bar", "BAZ=quux"]
        labels_data = {"com.example.vendor": "Acme", "com.example.license": "GPL",
                       "com.example.version": "1.0"}
        HostConfig = {"NetworkMode": "bridge"}
        try:

            r = swarm_client.create_container(image=image_data,
                                              command=cmd_data,
                                              name=instance_name)
            container_id = r.get('Id')
        except Exception as ex:
            logging.error("Error{}".format(ex))
            return None, ex
        created_at = datetime_to_timestamp(timezone.now())
        b = Instance(name=instance_name, created_at=created_at,
                     service=service, instance_id=instance_id,
                     continer_id=container_id,)
        #host='hostname'
        b.save()
        # container_id = json.loads(r.text).get('Id')
        print 'Create docker continer :{}'.format(instance_name)
        return container_id

    def start_continer(self, continer_id):
        logging.info('Start continer of: {}'.format(continer_id))

        try:
            requests.post(SWARM_URL + '/containers/{}/start'.format(continer_id))
        except Exception as ex:
            logging.error("Error: {}".format(ex))

    def delete_instance(self, continer_id):
        logging.info('Start continer of: {}'.format(continer_id))

        try:
            swarm_client.stop(container=continer_id)
            swarm_client.remove_container(container=continer_id)
        except Exception as ex:
            logging.error("Error: {}".format(ex))
        return True

