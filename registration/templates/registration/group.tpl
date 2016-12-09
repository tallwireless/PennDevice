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
        <li class='current_group'><a href="{% url 'reg:group' group.id %}">{{group.name}}</a></li>
    {% elif group.personal %}
        <li class='other_group'><a href="{% url 'reg:index' %}">Personal</a></li>
    {% else %}
        <li class='other_group'><a href="{% url 'reg:group' group.id %}">{{group.name}}</a></li>
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
<div class='button' onclick="showBlock('add_block','add_devices_block')">Add
new devices</div>
<div class='hidden' id='add_block'>
You currently have {{ available_device_count }} slots left for regisitration.
{% if get_info %}
{{get_info}}<br>
{% endif %}
{% if available_device_count != 0 %}
<form action="{% url 'reg:groupActionAddDevice' current_group.id %}"
method='POST' name='add_devices'>
{% csrf_token %}
<div class='device_table'>
    <div class='device_table_body'>
    <div class='device_table_header'>
        <div class='device_table_cell mac'>MAC Address</div>
        <div class='device_table_cell desc'>Description</div>
    </div>
    {% if get_info %} 

        {% for i in get_info.values %}
        {{ i }}
        {% if i.error %}
        <div class='device_table_row error'>
            <div class='device_table_cell mac'><input type='text' class='mac'
            value='{{ i.mac }}' name='mac-{{ i.index }}'><br><div
            class="form_error_message">{{ i.err_msg }}</div></div>
            <div class='device_table_cell desc'><input type='text' class='desc' value='{{ i.desc }}' name='desc-{{ i.index }}'></div>
        </div>
        {% endif %}
        {% endfor %}
    {% else %}

        {% for i in num_add_fields %}

        <div class='device_table_row' id='row-{{ i }}'>
            <div class='device_table_cell mac'>
            <input type='text' maxlength='17' class='mac' name='mac-{{ i }}' id='mac-{{ i }}' onblur="validateMac('{{ i }}')">
            <div id='mac-err-{{ i }}' class="form_error_message hidden">Please
            provide a vaild MAC address</div></div>
            <div class='device_table_cell desc'><input type='text' maxlength='255' class='desc' name='desc-{{ i }}'></div>
        </div>
        {% endfor %}
    {% endif %}
</div>
</div>


<input type='submit' value='Add Devices'>
</form>
{% endif %}
</div>

{% endblock %}
