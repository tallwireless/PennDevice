from django.conf.urls import url

from . import views
from .API.group import *
from .API.user import *
from .API.device import *
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
        name='APIGroupList'),
    url(r'api/groups/(?P<pk>[0-9]+)$',
        DeviceGroupAPI.as_view(),
        name='APIGroupView'),
    url(r'api/groups/(?P<action>all)$',
        DeviceGroupAPI.as_view(),
        name='APIGroupViewAll'),
    url(r'api/groups/(?P<pk>[0-9]+)/(?P<action>detail|members|devices|admins)$',
        DeviceGroupAPI.as_view(),
        name='APIGroupViewDetail'),
    url(r'api/users/$',
        UserAPI.as_view(),
        name='APIUserList'),
    url(r'api/users/(?P<username>[0-9a-zA-Z]+)/$',
        UserAPI.as_view(),
        name='APIUserDetail'),
    url(r'api/users/(?P<username>[0-9a-zA-Z]+)/(?P<action>groups)/$',
        UserAPI.as_view(),
        name='APIUserGroup'),
    url(r'api/devices/$',
        DeviceAPI.as_view(),
        name='APIDeviceList'),
    url(r'api/devices/(?P<mac>[0-9a-fA-f:]+)/$',
        DeviceAPI.as_view(),
        name='APIDeviceDetail'),
    url(r'logout/$',
        auth_views.logout,
        {'template_name': 'registration/logout.tpl'},
        name='logout'),
    ]

if settings.DEV == True:
    urlpatterns += [
        url(r'^.*login/$',
            auth_views.login,
            {'template_name': 'registration/login.tpl'},
            name='login'),
        ]

