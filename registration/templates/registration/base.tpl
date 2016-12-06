{% load static %}
<html>

<head>
<title>Penn Device - {% block page-title %} Home {% endblock %}</title>
<link rel="stylesheet" type="text/css" href="{% static 'registration/style.css' %}">
<script type="text/javascript">
{% block javascript %}
{% endblock %}
</script>
</head>


<body>
<div id='main'>
    <div class='header' id='header'>
        <span class='right-float'>{{ user }} (<a href="{% url 'reg:swapUser' %}">swap user</a>) | admin | logout</span>
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
