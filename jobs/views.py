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
from models import Job
from celery import task


# add.delay(2, 2)

def job_manage(request):
    print request
    if request.method == 'POST':
        render_to_response(
            'job_manage.html', {
                'username': request.user.username})

    else:

        return render_to_response(
            'job_manage.html', {
                'username': request.user.username})


def job_upload(request):
    if request.method == 'POST':
        # script= request.POST.get('script')
        # print type(script)
        # print request
        myFile = request.FILES.get('script', None)
        print '!!!!!!!!!!!!!!!'
        print(myFile._size)  # 文件大小字节数
        # bin_all = myFile.read()  # 一次过读取文件内容（会占很多内存）
        # for chunk in myFile.chuncks():
        #     fout.write(chunk)


        # if not myFile:
        #     return HttpResponse("no files for upload!")
        # destination = open(os.path.join("E:\\upload", myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        # for chunk in myFile.chunks():  # 分块写入文件
        #     destination.write(chunk)
        # destination.close()
        # return HttpResponse("upload over!"
        job_obj = Job()

        job_obj.service_name = 'mysc'
        job_obj.info = myFile
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
        script = ''
        agent = ''
        add_celery_job.delay(script, agent)

        return render_to_response('job_run.html', {'username': request.user.username})

    else:

        return render_to_response(
            'job_run.html', {
                'username': request.user.username})


@task()
def add_celery_job(script, agent):
    x = 1
    y = 2
    return x + y
