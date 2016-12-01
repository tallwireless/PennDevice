from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import *


def group(request, group_id=None):
    return HttpResponse("Soon to be showing group {}".format(group_id))

def groupAction(request, group_id):
    return HttpResponse("Soon to be showing group {}".format(group_id))
