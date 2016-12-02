from django.conf.urls import url

from . import views

app_name = 'reg'

urlpatterns = [
    url(r'^$', 
        views.group,
        name='index'),
    url(r'^group/(?P<group>.+)/$', 
        views.group,
        name='group'),
    url(r'^group/(?P<group>.+)/action/$', 
        views.groupAction,
        name='group_action'),
    url(r'^swapUser/$',
        views.swapUser,
        name="swapUser"),
    url(r'^swapUser/action/$',
        views.swapUserAction,
        name="swapUserAction"),
]
