<script>

var handleAddGroupForm = function(eventObj) {
    eventObj.preventDefault();
    var button = $(this).attr('id');
    if( button == 'cancel') {
        closeDialog();
    }
    if( button == 'save') {

        //Let make sure that at least the group name field has something in it
        var grp = $( "#grp" )[0].value;
        grp = grp.trim();
        var users = $( "#iUsers" )[0].value;
        console.log(users);
        users = users.split(" ");
        var special = $( "select#special option:selected" ).attr('value');
        console.log("grp: "+grp);
        if( grp == "") {
            $( "#row-grp" ).addClass("error");
            $( "#grp-err" ).removeClass("hidden");
            $( "#grp-err" ).html("Please provide a group name.");
            return 0;
        } else {
            $( "#row-grp" ).removeClass("error");
            $( "#grp-err" ).addClass("hidden");
        }

        //let's send it off for processing

        $.ajax({
            url: "/api/groups/",
            type: "PUT",
            data: JSON.stringify({ members: users, specialRole: special, name: grp }),
            datatype: "json",
            processData: false,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        })
        .done(handleGroupAdd)
            .fail(failedAjax);
    }
};

var handleGroupAdd = function(json) {
    if(json.error) {
        //We have an error
        $( "#row-grp" ).addClass("error");
        $( "#grp-err" ).removeClass("hidden");
        $( "#grp-err" ).html(json.err_msg);
        return 0;
    }
    closeDialog();
    $( "select#group" ).append("<option value='"+json.id+"'>"+json.name+"</option>");
    $( "select#group" ).val(json.id).change();
};

$( "#addGroup button" ).on("click", handleAddGroupForm);
</script>
<div class='addGroupForm'>
<form id='addGroup'>
<div class='fields'>
    <div class="row" id='row-grp'>
        <div class="label">Group Name</div>
        <div class="field"><input name='grp' id='grp' maxlength=32 size=25></div>
        <div id="grp-err" class="hidden"></div>
    </div>
    <div class="row" id='row-members'>
        <div class="label">Inital Members</div>
        <div class="field"><input name="users" id='iUsers' maxlength=254 size=30></div>
    </div>
    <div class="row" id='row-special'>
        <div class="label">Special VLAN/Role?</div>
        <div class="field"><select name='special'><option selected
        value='false'>No</option><option value='true'>Yes</option></select>
    </div>
</div>
<div class="buttons">
<button id='cancel'>Cancel</button><div class='float-right'><button id='save'>Save</button></div>
</div>
</div>
</div>
