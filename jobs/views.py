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
from django.shortcuts import render_to_response, render
from models import Job
from celery import task
from django import forms
import json
from services.models import Agent
from rest_framework.parsers import JSONParser, FormParser

logger = logging.getLogger(__name__)


def job_manage(request):
    if request.method == 'POST':
        # print request
        delete_job(request)

    scripts = Job.objects.all()
    # print scripts[0].job_name
    return render_to_response(
        'job_manage.html', {
            'username': request.user.username, 'show_list': scripts})


# def job_upload(request):
#     if request.method == 'POST':
#         # script= request.POST.get('script')
#         # print type(script)
#         # print request
#         myFile = request.FILES.get('script', None)
#
#         obj = request.FILES.get('script')
#         f = open(obj.name, 'wb')
#         for chunk in obj.chunks():
#             f.write(chunk)
#         f.close()
#         return Response(request)
#     else:
#
#             return render_to_response(
#                 'job_upload.html', {
#                     'username': request.user.username})

def job_upload(request):
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
        if Job.objects.filter(job_name=myFile).exists():
            return render_to_response('400.html', {'info': '脚本已经存在'})
        data = myFile.read()
        job_obj = Job()

        job_obj.job_name = save_name
        job_obj.info = data
        job_obj.describe = describe
        job_obj.save()
        return render_to_response(
            'job_upload.html', {
                'username': request.user.username})

    else:

        return render_to_response(
            'job_upload.html', {
                'username': request.user.username})


def job_run(request):
    if request.method == 'POST':
        # print request
        script_name = request.GET.get('job_name')

        if not script_name:
            return render_to_response('400.html')
        script_obj = Job.objects.filter(job_name=script_name)[0]
        agent_hosts_lis = request.POST.lists()
        for agent_host_set in agent_hosts_lis:
            agent = agent_host_set[0]
            print agent
            try:
                ip_addr = Agent.objects.get(host_name=agent).host_ip
            except:
                return render_to_response('400.html')
            script = script_obj.info

            headers = {'Accept': 'application/json'}
            # r = requests.post('http://127.0.0.1:8000', data=script, headers=headers)
            try:
                add_celery_job.delay(script, script_name, ip_addr)
            except Exception as e:
                logger.error(e)
                return render_to_response('400.html', {'info': '异步组件错误'})
                # r = requests.post('http://10.6.168.161:8000', data=script, headers=headers)

        return render_to_response('job_manage.html')

    else:
        scripts = Job.objects.all()
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


def delete_job(request):
    post_jobs = request.POST.getlist('post_jobs')
    for job_name in post_jobs:
        logger.debug('Start delete script :{}'.format(job_name))
        try:
            job_obj = Job.objects.get(job_name=job_name)
            job_obj.delete()
        except Exception as ex:
            # return Response(
            #     'Service dose not exit. {}'.format(ex),
            #     status=status.HTTP_400_BAD_REQUEST)
            return render_to_response('400.html')


def job_periodictask(request):
    if request.method == 'POST':
        pass
    else:
        return render_to_response('job_periodictask.html')


@task()
def add_celery_job(script, script_name, ip_addr):
    headers = {'Accept': 'application/json'}
    r = requests.post('http://{0}:8000/job/{1}'.format(ip_addr, script_name), data=script, headers=headers)
    print 'success'
    print r

    # return r.text


def call_agent_change_ip(agent_ip, instance_name, assignment_ip, subnet_mask, gateway_ip):
    headers = {'Accept': 'application/json'}
    script = {"instance_name": instance_name, "assignment_ip": assignment_ip,
              "subnet_mask": subnet_mask, "gateway_ip": gateway_ip}
    r = requests.post('http://{0}:8000/assignment_ip'.format(agent_ip), data=script, headers=headers)
    print r
