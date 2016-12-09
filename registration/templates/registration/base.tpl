{% load static %}
<html>

<head>
<title>Penn Device - {% block page-title %} Home {% endblock %}</title>
<link rel="stylesheet" type="text/css" href="{% static 'registration/style.css' %}">
<script src="{% static 'registration/site.js' %}"></script>
</head>


<body>
<div id='main'>
    <div class='tb-common header'>
        {% if user.is_authenticated %}
        <div class='info-bar float-right'>{{ user.first_name  }} {{ user.last_name }}
        ({{ user.email }}) | <a href="{% url 'reg:logout' %}">logout</a></div>
        {% else %}
        <div class='info-bar float-right'><a href="{% url 'reg:login'
        %}">login</a></div>
        {% endif %}
        <span class='site-title'>PennDevice</span><br/>
        <span class='subtitle'>{% block subtitle %} Home {% endblock %}</span>
    </div>
    <div class='content'>
        {% block content %}

        fancy content here.

        {% endblock content %}
    </div>
    <div class='tb-common footer'>
    A quick development by Charles
    </div>
</div>
</body>
</html>
