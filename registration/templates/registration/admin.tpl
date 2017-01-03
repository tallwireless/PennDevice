
{% extends "./base.tpl" %}
{% load static %}

{% block subtitle %}Administration{% endblock %}

{% block includes %}
<script src="{% static 'registration/admin.js' %}"></script>
{% endblock %}

{% block content %}
<ul class='tab_set'>
        <li class='tab selected'><a href="javascript:void(null)">Groups</a></li>
        <li class='tab'><a href="javascript:void(null)">Users</a></li>
        <li class='tab'><a href="javascript:void(null)">Devices</a></li>
        <li class='tab'><a href="javascript:void(null)">Blacklist</a></li>
</ul>
<div id='page_block'>
</div>
{% endblock %}
