from django.conf.urls import url

from . import views
from django.contrib.auth import views as auth_views


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
    url(r'login_auth/$',
        auth_views.login,
        {'template_name': 'registration/login.tpl'},
        name='login_auth'),
    url(r'logout/$',
        auth_views.logout,
        {'template_name': 'registration/logout.tpl'},
        name='logout'),
        url(r'ajax/$',
                    views.ajaxHandler,
                            name='ajaxHandler'),
    ]
