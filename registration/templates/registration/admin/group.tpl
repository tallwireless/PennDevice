<div class='select_container'>
    <form id='admin-select-group'>
Please select a group to manage: <select id='group'>
        {% for group in groups %}
            <option value='{{ group.id }}'>{{ group.name }}</option>
        {% endfor %}
    </select>
    </form>
</div>
<div class='deviceTable-wrapper'>
    <span class='header'>Devices</span>
    <table id='deviceTable' class='deviceTable display compact'></table>
</div>
<div class='groupMembers-wrapper'>
    <span class='header'>Users</span>
    <table id='groupMembers' class='deviceTable display compact'></table>
</div>
