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

<div class='table device_table'>
    <div class='body'>
    <div class='header'>
        <div class='cell mac'>MAC Address</div>
        <div class='cell desc'>Description</div>
        <div class='cell added'>Date Added</div>
        <div class='cell expire'>Date Expire</div>
        {% if not current_group.personal %}
        <div class='cell added_by'>Added By</div>
        {% endif %}
        <div class='cell action'>Action</div>
    </div>
    {% for device in devices %}
    <div class='row' id='{{ device.pk }}'>
        <div class='cell mac' id='{{ device.pk }}-mac'>{{ device.pk }}</div>
        <div class='cell desc' id='{{ device.pk }}-des'>{{ device.description }} </div>
        <div class='cell added' id='{{ device.pk }}-add'>{{ device.added.date }}</div>
        <div class='cell expire' id='{{ device.pk }}-exp'>{{ device.expires.date }}</div>
        {% if not current_group.personal %}
        <div class='cell added_by' id='{{ device.pk }}-usr'>{{ device.added_by }}</div>
        {% endif %}
        <div class='cell action' id='{{ device.pk }}-action'><a
        href="javascript:void(0)" id='{{ device.pk }}-del'>Del</a>&nbsp;|&nbsp;<a
        href="javascript:void(0)" id='{{ device.pk }}-renew'>Renew</a></div>
    </div>
    {% endfor %}
    </div>
</div>
<div class='container'>
<div class='button' id='add_devices_form'> Add new devices</div> 
{% if is_admin %}<div class='button' id='admin_group'>Administer Group</div>{% endif %}
<div class='' id='block'> </div>


</div>
{% endblock %}
