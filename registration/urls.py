from django.conf.urls import url

from . import views
from .API.group import *
from django.contrib.auth import views as auth_views

from socket import gethostname
from django.conf import settings

app_name = 'reg'

urlpatterns = [
    url(r'^$', 
        views.group,
        name='index'),
    url(r'^group/(?P<group_id>[0-9]+)$', 
        views.group,
        name='group'),
    url(r'^group/(?P<group_id>[0-9]+)/action/add_device/$', 
        views.groupActionAdd,
        name='groupActionAddDevice'),
    url(r'ajax/$',
        views.ajaxHandler,
        name='ajaxHandler'),
    url(r'api/groups/$',
        DeviceGroupAPI.as_view(),
        name='APIgroupView'),
    url(r'api/groups/(?P<pk>[0-9]+)$',
        DeviceGroupAPI.as_view(),
        name='APIgroupView'),
    url(r'api/groups/(?P<action>all)$',
        DeviceGroupAPI.as_view(),
        name='APIgroupViewAll'),
    url(r'api/groups/(?P<pk>[0-9]+)/(?P<action>detail|members|devices|admins)$',
        DeviceGroupAPI.as_view(),
        name='APIgroupViewDetail'),
    ]

if settings.DEV == True:
    urlpatterns += [
        url(r'^.*login/$',
            auth_views.login,
            {'template_name': 'registration/login.tpl'},
            name='login'),
        url(r'logout/$',
            auth_views.logout,
            {'template_name': 'registration/logout.tpl'},
            name='logout'),
        ]

print(urlpatterns)
