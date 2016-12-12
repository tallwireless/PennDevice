<div class='table group-user'>
    <div class='body'>
        <div class='row header'>
            <div class='name'>Name</div>
            <div class='username'>PennKey</div>
            <div class='group-admin'>Admin</div>
        </div>
        {% for member in members %}
            <div class='row'>
                <div class='name'>{{ member.name }}</div>
                <div class='username'>{{ member.username }}</div>
                <div class='group-admin'>{% if member.group_admin %}Yes{% else %}No{% endif %}</div>
            </div>
        {% endfor %}
    </div>
</div>
