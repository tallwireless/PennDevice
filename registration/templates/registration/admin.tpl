
{% extends "./base.tpl" %}
{% load static %}

{% block subtitle %}Administration{% endblock %}

{% block includes %}
<script src="{% static 'registration/admin.js' %}"></script>
{% endblock %}

{% block content %}
<script>

var readyFunction = function() {
    console.log("Starting...");
    registerEvents();
    fetchContent('groups','admin');
    $( "#dialog" ).dialog({autoOpen:false, "modal": true} );

};

$(document).ready(readyFunction);
</script>
<ul class='tab_set'>
        <li class='tab selected' id='groups'><a href='javascript:void(null)'>Groups</a></li>
        <li class='tab' id='users'><a href="javascript:void(null)">Users</a></li>
        <li class='tab' id='devices'><a href="javascript:void(null)">Devices</a></li>
        <li class='tab' id='blacklist'><a href="javascript:void(null)">Blacklist</a></li>
</ul>
<div id='page_block'>
</div>
{% endblock %}
