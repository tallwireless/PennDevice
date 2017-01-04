{% load static %}
<!DOCTYPE html>
<html>

<head>
<title>Penn Device - {% block page-title %} Home {% endblock %}</title>
<link rel="stylesheet" type="text/css" href="{% static 'registration/style.css' %}">
<link rel="stylesheet" type="text/css" href="{% static 'registration/jquery-ui.min.css' %}">
<link rel="stylesheet" type="text/css" href="{% static 'registration/jquery.dataTables.min.css' %}">
<script src="{% static 'registration/jquery.js' %}"></script>
<script src="{% static 'registration/jquery.dataTables.min.js' %}"></script>
<script src="{% static 'registration/jquery-ui.min.js' %}"></script>
{% block includes %}<!--There are no page specific includes-->{% endblock %}
</head>


<body>
<div class='main'>
    <div class='tb-common header'>
        {% if user.is_authenticated %}
        <div class='info-bar float-right'>{{ user.first_name  }} {{ user.last_name }} 
        ({{ user.email }}) | <a href='{% url 'reg:index' %}'>Home</a>
        {% if site_admin %} | <a href='{% url 'reg:admin' %}'>Administration</a> {% endif %}
        | <a href="{% url 'reg:logout' %}">logout</a></div>{% else %}
        <div class='info-bar float-right'><a href="{% url 'reg:index' %}">login</a></div>
        {% endif %}
        <span class='site-title'>PennDevice</span><br/>
        <span class='subtitle'>{% block subtitle %} Home {% endblock %}</span>
    </div>
    <div class='content'>
        <div id='statMsgBox' class='hidden'>
            <div class='title'>test</div>
            <div class='message'>this is a test message.</div>
        </div>
        
        {% block content %}

        fancy content here.

        {% endblock content %}
    </div>
    <div class='tb-common footer'>
    A quick development by Charles | Code can be found on <a
    href='https://github.com/tallwireless/PennDevice'>GitHub</a>
    </div>
</div>
</body>
</html>
