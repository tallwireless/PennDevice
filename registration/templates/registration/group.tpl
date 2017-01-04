{% extends "./base.tpl" %}
{% load static %}
{% block subtitle %}Edit Devices{% endblock %}

{% block includes %}
<script src="/static/registration/group.js"></script>
{% endblock %}

{% block content %}

<ul class='tab_set'>
{% for group in groups %}
    {% if group == current_group and group.personal %}
        <li class='tab selected'><a href="{% url 'reg:index' %}">Personal</a></li>
    {% elif group == current_group %}
        <li class='tab selected'><a href="{% url 'reg:group' group.id %}">{{ group.name }}</a></li>
    {% elif group.personal %}
        <li class='tab' id='grp-{{ group.id }}'>
        <a href="{% url 'reg:index' %}">Personal</a></li>
    {% else %}
        <li class='tab' id='grp-{{ group.id }}'>
                <a href="{% url 'reg:group' group.id %}">{{group.name}}</a>
            </li>
    {% endif %}
{% endfor %}
</ul>

{% if admin_str %}
The administrators for this group are: {{ admin_str }}
{% endif %}
<div class='deviceTable-wrapper'>
<table id='deviceTable' class='deviceTable display compact' cellspacing="0">
</table>
</div>
<div class='container'>
<div class='button' id='add_devices_form'> Add new devices</div> 
{% if is_admin %}<div class='button' id='admin_group'>Administer Group</div>{% endif %}
<div id='statMsgBoxBlock' class='hidden'>
<div class='title'></div><div class='message'></div>
</div>
<div class='' id='block'> </div>


</div>
{% endblock %}
