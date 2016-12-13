<script src='/static/registration/add_device_form.js'>
</script>
You currently have {{ available_device_count }} slots left for regisitration.
{% if get_info %}
{{get_info}}<br>
{% endif %}
{% if available_device_count != 0 %}
<form  name='add_devices'>
<div class='table add_device_table'>
    <div class='body'>
    <div class='header'>
        <div class='cell mac'>MAC Address</div>
        <div class='cell desc'>Description</div>
    </div>
    {% for i in num_add_fields %}
        <div class='row' id='row-{{ i }}'>
            <div class='cell mac'>
                <input type='text' maxlength='17' class='mac' name="mac-{{ i }}">
                <div id='mac-err-{{ i }}' class="form_error_message hidden">
                    Please provide a vaild MAC address
                </div>
            </div>
            <div class='cell desc'>
                <input type='text' maxlength='255' class='desc' name='des-{{ i }}'>
            </div>
        </div>
    {% endfor %}
</div>
<input type='submit' value='Add Devices'>
</form>
{% endif %}
</div>
