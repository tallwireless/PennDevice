{% extends "./base.tpl" %}

{% block subtitle %}Edit Devices{% endblock %}

{% block javascript %}
function showAddDevices() {
    document.getElementById('add_devices_block').style.display = "block";
}
{% endblock %}

{% block content %}

<ul class='group_list'>
{% for group in groups %}
    {% if group == current_group and group.personal %}
        <li class='current_group tab'><a href="{% url 'reg:index' %}">Personal</a></li>
    {% elif group == current_group %}
        <li class='current_group tab'><a href="{% url 'reg:group' group.id %}">{{ group.name }}</a></li>
    {% elif group.personal %}
        <li class='other_group tab' id='grp-{{ group.id }}'>
        <a href="{% url 'reg:index' %}">Personal</a></li>
    {% else %}
        <li class='other_group tab' id='grp-{{ group.id }}'>
                <a href="{% url 'reg:group' group.id %}">{{group.name}}</a>
            </li>
    {% endif %}
{% endfor %}
</ul>

<div id='statMsgBox' class='hidden'>
<div class='title'></div><div class='message'></div>
</div>
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
<div class='' id='block'> </div>


</div>
{% endblock %}
