<div class='select_container'>
    <form id='admin-select-group'>
Please select a group to manage: <select id='group'>
        {% for group in groups %}
            <option value='{{ group.id }}'>{{ group.name }}</option>
        {% endfor %}
    </select>
    </form>
</div>
<div class='admin-tables-wrapper'>
    <div class='deviceTable-wrapper'>
        <span class='header'>Devices</span>
        <table id='deviceTable' class='deviceTable display compact'></table>
    </div>
        <span class='header'>Users</span>
    <div class='membersTable-wrapper'>
        <table id='membersTable' class='deviceTable display compact'></table>
    </div>
</div>
