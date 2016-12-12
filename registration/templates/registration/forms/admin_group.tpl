<div class='table group-user'>
    <div class='body'>
        <div class='row header'>
            <div class='cell name'>Name</div>
            <div class='cell username'>PennKey</div>
            <div class='cell group-admin'>Admin</div>
        </div>
        {% for member in members %}
            <div class='row'>
                <div class='cell name'>{{ member.name }}</div>
                <div class='cell username'>{{ member.username }}</div>
                <div class='cell group-admin'>{% if member.group_admin %}Yes{% else %}No{% endif %}</div>
            </div>
        {% endfor %}
    </div>
</div>
