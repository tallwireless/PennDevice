from .models import *

import json
import requests
from pprint import pprint as pp

class PacketFence(object):
    def __init__(self,something=None):
        self.url = "https://{}:{}/".format(
                    Setting.objects.get(pk='packetfence.address').value,
                    Setting.objects.get(pk='packetfence.port').value )
        self.auth = ( Setting.objects.get(pk='packetfence.username').value,
                      Setting.objects.get(pk='packetfence.password').value)
        self.headers = {"content-type": "application/json"}

    def get_user(self,username):
        payload = [ username ]
        return self.__fetch_data('view_person',payload)

    def modify_user(self,data):
        fix_data = []
        for d in data:
            fix_data.append(d)
            fix_data.append(data[d])
        return self.__fetch_data('modify_person',fix_data)

    def add_user(self,username):
        payload = ["pid", username ]
        return self.__fetch_data('add_person',payload)
    
    def get_node(self,device):
        mac = device.pk
        payload = ["mac", mac ]
        return self.__fetch_data('node_information',payload)

    def add_node(self,device,group):
        mac = device.pk
        duration = ""
        role = Setting.objects.get(pk="packetfence.personal.default_role").value
        if group.personal:
            duration = Setting.objects.get(pk="packetfence.duration.personal").value
        else:
            duration = Setting.objects.get(pk="packetfence.duration.nonpersonal").value
            if group.specialRole:
                role="Group_"+group.name.replace(" ","-")
        
        payload = ['mac', mac, 'category', role, 'status', 'reg', 'pid', group.name]
        return self.__fetch_data('modify_node', payload)
    
    def del_node(self,device):
        # there is no delete node call, so we'll place it in the REJECT role
        # for now and then let packetfence clean it up
        mac = device.pk

        payload = ['mac', mac] 
        return self.__fetch_data('delete_node', payload)

    def __fetch_data(self,method,payload):
        payload = { "jsonrcp": "2.0",
                    "params": payload }
        response = requests.post(self.url+method,
                data=json.dumps(payload), headers=self.headers,
                auth=self.auth)
        return response.json()
