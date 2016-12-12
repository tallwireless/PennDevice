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
        <li class='current_group'><a href="{% url 'reg:index' %}">Personal</a></li>
    {% elif group == current_group %}
        <li class='current_group'><a href="{% url 'reg:group' group.id
        %}">{{group.name}}</a></li>
    {% elif group.personal %}
        <li class='other_group' onmouseenter="highlight('grp-{{ group.id }}')"
        onmouseleave="highlight('grp-{{ group.id }}')" id='grp-{{ group.id }}'>
        <a href="{% url 'reg:index' %}">Personal</a></li>
    {% else %}
        <li class='other_group' onmouseenter="highlight('grp-{{ group.id }}')"
                onmouseleave="highlight('grp-{{ group.id }}')" id='grp-{{ group.id }}'>
                <a href="{% url 'reg:group' group.id %}">{{group.name}}</a>
            </li>
    {% endif %}
{% endfor %}
</ul>

<div class='device_table'>
    <div class='device_table_body'>
    <div class='device_table_header'>
        <div class='device_table_cell mac'>MAC Address</div>
        <div class='device_table_cell desc'>Description</div>
        <div class='device_table_cell added'>Date Added</div>
        <div class='device_table_cell expire'>Date Expire</div>
        {% if not current_group.personal %}
        <div class='device_table_cell added_by'>Added By</div>
        {% endif %}
        <div class='device_table_cell del'>Delete?</div>
    </div>
    {% for device in devices %}
    <div class='device_table_row' id='{{ device.pk }}'>
        <div class='device_table_cell mac' id='{{ device.pk }}-mac'>{{ device.pk }}</div>
        <div class='device_table_cell desc' id='{{ device.pk }}-des'>{{ device.description }} </div>
        <div class='device_table_cell added' id='{{ device.pk }}-add'>{{ device.added.date }}</div>
        <div class='device_table_cell expire' id='{{ device.pk }}-exp'>{{ device.expires.date }}</div>
        {% if not current_group.personal %}
        <div class='device_table_cell added_by' id='{{ device.pk }}-usr'>{{ device.added_by }}</div>
        {% endif %}
        <div class='device_table_cell del' id='{{ device.pk }}-del'><a
        href='{% url 'reg:deviceDel' device.pk %}'>delete</a></div>
    </div>
    {% endfor %}
    </div>
</div>
<div class='container'>
<div class='button' id='add_divices'> Add new devices</div> 
{% if is_admin %}<div class='button' id='admin_group'>Administer Group</div>{% endif %}
<div class='' id='block'> </div>


</div>
{% endblock %}
