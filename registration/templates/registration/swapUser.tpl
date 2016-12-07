{% extends "./base.tpl" %}

{% block subtitle %}Testing: Swap User{% endblock %}

{% block content %}
{% if error_message %}
<div class='error'><div class='error-title'>Error</div>
<p class='error-message'>{{ error_message }}</p></div>
{% endif %}

<h1>Switch User<h2>

<h3>Current User: {{ user }}</h3>

<form action="{% url 'reg:swapUserAction' %}" method=POST>
{% csrf_token %}
<h3>Change User: <select name="new_user">
{% for new_user in user_list %}
    {% if new_user.pennkey == user %}
        <option value="{{ new_user.pk }}" selected>{{ new_user.pennkey }}</option>
    {% else %}
        <option value="{{ new_user.pk }}">{{ new_user.pennkey }}</option>
    {% endif %}
{% endfor %}
</select>
<input type="submit" value="change" />
</form>

{% endblock content %}
        
