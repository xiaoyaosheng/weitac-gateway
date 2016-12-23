# coding=utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from login.models import User
from django import forms
from rest_framework.response import Response
from rest_framework import status
import requests

# 定义表单模型
class UserForm(forms.Form):
    username = forms.CharField(label='用户名：', max_length=100)
    password = forms.CharField(label='密码：', widget=forms.PasswordInput())


# 登录
def login(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            # 获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # 获取的表单数据与数据库进行比较
            user = User.objects.filter(username__exact=username, password__exact=password)
            if user:
                return HttpResponseRedirect('/swarm/')
                # return render_to_response('success_create.html', {'username': username})
            else:
                return HttpResponseRedirect('/login/')
    else:
        uf = UserForm()
    return render_to_response('login.html', {'uf': uf})


class CreateForm(forms.Form):
    service_name = forms.CharField(label='服务名：', max_length=100)
    image_name = forms.CharField(label='镜像：', max_length=100)


class DeleteForm(forms.Form):
    service_name = forms.CharField(label='服务名：', max_length=100)


def create(request):

    if request.method == 'POST':
        uf = CreateForm(request.POST)
        if uf.is_valid():
            # 获取表单用户密码
            service_name = uf.cleaned_data['service_name']
            image_name = uf.cleaned_data['image_name']
            data={
                    "service_name":"myweb",
                    "image_name":"ubuntu",
                    "instance_amount":"1",
                    "detail":""
                    }
            requests.post('http://127.0.0.1:8080/services',data=data)
            # return Response("success",
            #                 status=status.HTTP_200_OK)
            return render_to_response('success_create.html')
    else:
        uf = CreateForm()
    return render_to_response('swarm.html', {'uf':uf})


def swarm(request):
    uf = CreateForm()
    de_uf=DeleteForm()
    return render_to_response('swarm.html', {'uf': uf,'de_uf':de_uf})


def success(request,**kwargs):
    back_type = str(kwargs['type'])
    print back_type
    if back_type=='1':
        uf = CreateForm(request.POST)

        if uf.is_valid():
            # 获取表单用户密码
            service_name = uf.cleaned_data['service_name']
            image_name = uf.cleaned_data['image_name']
            data = {
                "service_name": service_name,
                "image_name": "ubuntu",
                "instance_amount": "1",
                "detail": ""
            }
            requests.post('http://127.0.0.1:8080/services', data=data)
            # return Response("success",
            #                     status=status.HTTP_200_OK)
            return render_to_response('success_create.html')
    if back_type=='2':
        de_uf = DeleteForm(request.POST)

        if de_uf.is_valid():

            # 获取表单用户密码
            service_name = de_uf.cleaned_data['service_name']
            print service_name
            data = {
                "service_name": service_name,
                "image_name": "ubuntu",
                "instance_amount": "1",
                "detail": ""
            }
            requests.delete('http://127.0.0.1:8080/services', data=data)
            # return Response("success",
            #                     status=status.HTTP_200_OK)
            return render_to_response('success_delete.html')