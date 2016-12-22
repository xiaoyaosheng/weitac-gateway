from rest_framework import serializers
from services.models import Service, IpInfo
from django.contrib.auth.models import User



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User


class ServiceSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(source='app_info.username')
    # region = serializers.CharField(source='app_info.region_info')

    class Meta:
        model = Service
        fields = ('service_name', 'instance_amount', 'image_name', 'created_at',
                  'updated_at', 'finished_at')

    def create(self):
        return Service(**self.object)