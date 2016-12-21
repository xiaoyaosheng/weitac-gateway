from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import viewsets
from models import Service,Instance
from services.serializers import ServiceSerializer
from rest_framework import permissions
import datetime
import logging
import requests
import base64
from django.db.models import Q
from django.http import HttpResponse

logger = logging.getLogger(__name__)
import json
from services.settings import SWARM_URL
from services.serializers import ServiceSerializer


def hello(request):
    return HttpResponse(u"hello")


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
        if not Service.objects.filter(service_name=data['service_name']).exists():
            #serializer.save()
            continer_id= self.create_continer(data['service_name'])
            print continer_id
            self.start_continer(continer_id)
        else:
            print 'Service {} exits'.format(data['service_name'])
            return Response('Service {} exits. Do you want to add more instances? Please use update API'.format(
                data['service_name']), status=status.HTTP_400_BAD_REQUEST)
    # except Exception as ex:
        #     print ex.message

        print 'success'
        return Response('success', status=status.HTTP_200_OK)
        # logging.debug('object after serialized: {}'.format(service))

    def create_continer(self, request, **kwargs):
        logger.info('Create a service: {}'.format(request))

        env_data = ["FOO=bar", "BAZ=quux"]
        cmd_data = ["nginx",
                    "-g",
                    "daemon off;"]
        image_data = "nginx"
        labels_data = {"com.example.vendor": "Acme", "com.example.license": "GPL",
                       "com.example.version": "1.0"}
        HostConfig = {"NetworkMode": "bridge"}

        data_body = {"Env": env_data, "Cmd": cmd_data, "Image": image_data,
                     "Labels": labels_data, "HostConfig": HostConfig}

        try:
            r = requests.post(SWARM_URL + '/containers/create', data=json.dumps(data_body))
            print r.text
        except Exception as ex:
            logging.error("swarm url is wrong{}".format(ex))
        return json.loads(r.text).get('Id')
        # return Response('success', status=status.HTTP_200_OK)

    def start_continer(self, continer_id):
        logging.info('Start continer of: {}'.format(continer_id))

        try:
            r = requests.post(SWARM_URL + '/containers/{}/start'.format(continer_id))
            print r.text
        except Exception as ex:
            logging.error("can't get the amount of instance_id in this ur! error: {}".format(ex))





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


class Instance():
    model = Instance

    def create_continer(self, request, **kwargs):
        logger.info('Create a service: {}'.format(request))

        env_data = ["FOO=bar", "BAZ=quux"]
        cmd_data = ["nginx",
                    "-g",
                    "daemon off;"]
        image_data = "nginx"
        labels_data = {"com.example.vendor": "Acme", "com.example.license": "GPL",
                       "com.example.version": "1.0"}
        HostConfig = {"NetworkMode": "bridge"}

        data_body = {"Env": env_data, "Cmd": cmd_data, "Image": image_data,
                     "Labels": labels_data, "HostConfig": HostConfig}

        try:
            r = requests.post(SWARM_URL + '/containers/create', data=json.dumps(data_body))
            print r.text
        except Exception as ex:
            logging.error("swarm url is wrong{}".format(ex))
        return json.loads(r.text).get('Id')
        # return Response('success', status=status.HTTP_200_OK)

    def start_continer(self, continer_id):
        logging.info('Start continer of: {}'.format(continer_id))

        try:
            r = requests.post(SWARM_URL + '/containers/{}/start'.format(continer_id))
            print r.text
        except Exception as ex:
            logging.error("can't get the amount of instance_id in this ur! error: {}".format(ex))




if __name__ == '__main__':
    ServiceViewSet.start_continer('78')
