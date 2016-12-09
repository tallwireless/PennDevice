{% load static %}
<html>

<head>
<title>Penn Device - {% block page-title %} Home {% endblock %}</title>
<link rel="stylesheet" type="text/css" href="{% static 'registration/style.css' %}">
<script src="{% static 'registration/site.js' %}"></script>
</head>


<body>
<div id='main'>
    <div class='header' id='header'>
        {% if user.is_authenticated %}
        <span class='right-float'>{{ user.first_name  }} {{ user.last_name }}
        ({{ user.email }}) | <a href="{% url 'reg:logout' %}">logout</a></span>
        {% else %}
        <span class='right-float'><a href="{% url 'reg:login' %}">login</a></span>
        {% endif %}
        <span class='site-title'>PennDevice</span><br/>
        <span class='subtitle'>{% block subtitle %} Home {% endblock %}</span>
    </div>
    <div class='content'>
        {% block content %}

        fancy content here.

        {% endblock content %}
    </div>
    <div class='bottom'>
    A quick development by Charles
    </div>
</div>
</body>
</html>
