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
docker_client = docker.APIClient(base_url='tcp://10.6.168.160:2376',timeout=10)

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
        service_name=data['service_name']
        instance_amount=data['instance_amount']
        print type(instance_amount)
        if not Service.objects.filter(service_name=service_name).exists():
            instance=Instance_event()
            for i in range(int(instance_amount)):
                instance_name=service_name+'_{}'.format(i)
                instance.create_continer(instance_name)
                instance.start_continer(instance_name)
                    # print 'created docker\' continer_id is Null'
                    # return Response('Service Error', status=status.HTTP_400_BAD_REQUEST)
        else:
            print 'Service {} exits'.format(service_name)
            return Response('Service {} exits. Do you want to add more instances? Please use update API'.format(
                data['service_name']), status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        created_at = datetime_to_timestamp(timezone.now())
        service_obj = Service.objects.get(service_name=service_name)
        service_obj.created_at = created_at
        service_obj.save()
        return Response('success', status=status.HTTP_200_OK)
        # logging.debug('object after serialized: {}'.format(service))





            # def update_services(self, request, ** kwargs):
            #     data = request.DATA
            #     logger.info('get user msg:{}'.format(data))
            #     app_id = data['app_id']
            #     order = data['event_type']
            #     logger.debug('get app order {}'.format(data))
            #     if order == 'START' or order == 'CREATE':
            #         logger.info('create {} volume by JAKIRO'.format(app_id))
            #         create_volume_event(app_id, 'JAKIRO')
            #         if order == 'CREATE' and not AppSizeInfo.objects.filter(app_id=app_id).exists():
            #             appinfo = AppSizeInfo(app_id=app_id)
            #             appinfo.size = data['size']
            #             appinfo.username = data['username']
            #             appinfo.region_info = data['region']
            #             appinfo.save()
            #     if order == 'UPDATE':
            #         if not AppSizeInfo.objects.filter(app_id=app_id).exists():
            #             appinfo = AppSizeInfo(app_id=app_id)
            #             appinfo.size = data['size']
            #             appinfo.username = data['username']
            #             appinfo.region_info = data['region']
            #             appinfo.save()
            #         else:
            #             appinfo = AppSizeInfo.objects.get(app_id=app_id)
            #             if appinfo.size != data['size']:
            #                 appinfo.size = data['size']
            #                 appinfo.save()
            #     if order == 'DESTROY':
            #         finish_volume_event(app_id)
            #
            #     t = timezone.now()
            #     stnamp = int(time.mktime(t.timetuple()))
            #     if not Event.objects.filter(app_id=app_id).exists():
            #         return Response("app:%s not exist" % app_id,
            #                         status=status.HTTP_400_BAD_REQUEST)
            #
            #     if order == "STOP" or order == "DESTROY":
            #         Event.objects.filter(app_id=app_id,
            #                              finished_at=0).update(finished_at=stnamp)
            #     return Response("success",
            #                     status=status.HTTP_200_OK)



            # def delete_services(self, request, **kwargs):
            #     serializer = TaskSerializer(data=request.DATA)
            #     if not serializer.is_valid():
            #         return Response(serializer.errors,
            #                         status=status.HTTP_400_BAD_REQUEST)
            #     task = serializer.create()
            #     logger.debug('object after serialized: {}'.format(task))
            #     Event.objects.filter(app_id=task.app).delete()
            #     return Response('success',
            #                     status=status.HTTP_200_OK)
            #
            #
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
            #


class Instance_event():
    model = Instance

    def create_continer(self, instance_name):
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
            # r = requests.post(SWARM_URL + '/containers/create?name', data=json.dumps(data_body))
            container_id=docker_client.create_container(image=image_data,
                              command=cmd_data, name=instance_name)
        except Exception as ex:
            logging.error("swarm url is wrong: {}".format(ex))
            return None
        b = Instance(service_name=instance_name,
                     instance_id='',created_at='',host_name='')
        b.save()
        # container_id = json.loads(r.text).get('Id')
        print 'Create docker continer :{}'.format(instance_name)


    def start_continer(self, continer_id):
        logging.info('Start continer of: {}'.format(continer_id))

        try:
            requests.post(SWARM_URL + '/containers/{}/start'.format(continer_id))
        except Exception as ex:
            logging.error("Error: {}".format(ex))


if __name__ == '__main__':
    ServiceViewSet.start_continer('78')
