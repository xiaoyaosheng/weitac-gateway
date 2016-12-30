from django.shortcuts import render

# Create your views here.
from jobs.tasks import add


add.delay(2, 2)