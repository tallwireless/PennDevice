from django.conf.urls import url

from . import views

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
    url(r'^swapUser/$',
        views.swapUser,
        name="swapUser"),
    url(r'^swapUser/action/$',
        views.swapUserAction,
        name="swapUserAction"),
]
