You currently have {{ available_device_count }} slots left for regisitration.
{% if get_info %}
{{get_info}}<br>
{% endif %}
{% if available_device_count != 0 %}
<form action="{% url 'reg:groupActionAddDevice' current_group.id %}"
method='POST' name='add_devices'>
{% csrf_token %}
<div class='table add_device_table'>
    <div class='body'>
    <div class='header'>
        <div class='cell mac'>MAC Address</div>
        <div class='cell desc'>Description</div>
    </div>
    {% if get_info %} 

        {% for i in get_info.values %}
        {{ i }}
        {% if i.error %}
        <div class='row error'>
            <div class='cell mac'><input type='text' class='mac'
            value='{{ i.mac }}' name='mac-{{ i.index }}'><br><div
            class="form_error_message">{{ i.err_msg }}</div></div>
            <div class='cell desc'><input type='text' class='desc' value='{{ i.desc }}' name='desc-{{ i.index }}'></div>
        </div>
        {% endif %}
        {% endfor %}
    {% else %}

        {% for i in num_add_fields %}

        <div class='row' id='row-{{ i }}'>
            <div class='cell mac'>
            <input type='text' maxlength='17' class='mac' name='mac-{{ i }}' id='mac-{{ i }}' onblur="validateMac('{{ i }}')">
            <div id='mac-err-{{ i }}' class="form_error_message hidden">Please
            provide a vaild MAC address</div></div>
            <div class='cell desc'><input type='text' maxlength='255' class='desc' name='desc-{{ i }}'></div>
        </div>
        {% endfor %}
    {% endif %}
</div>
<input type='submit' value='Add Devices'>
</form>
{% endif %}
</div>
