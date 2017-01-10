<script>

var handleAddUserForm = function (eventObj) {
    /* This is to handle submitting the Add User Form. */
    eventObj.preventDefault();
    var button = $(this).attr('id');
    if( button == 'cancel') {
        /* if the user hits cancel, let's make the dialog go away. */
        closeDialog();
        return 0;
    }
    if( button == 'saveadd' || button == 'save') {
        /* let's check to make sure that we have SOMETHING */
        var pennkey = $( "#pennkey" )[0].value;
        var valid_pennkey = /[0-9a-zA-Z]{2,}/i;
        if( ! valid_pennkey.test(pennkey) ) {
            /* we have an error. Let's let the user know. */
            $( "#row-user" ).addClass("error");
            $( "#user-err" ).removeClass('hidden');
            $( "#user-err" ).html("Please provide a valid PennName.");
            return 0;
        } else {
            /* no error. Make sure we clean up after the old error. */
            $( "#row-user" ).removeClass("error");
            $( "#user-err" ).addClass('hidden');
            $( "#user-err" ).html("");
        }
        /* send the put request off to the server */
        $.ajax({
            url: "/api/groups/"+getCurrentGroup()+"/members/"+pennkey,
            type: "PUT",
            datatype: "json",
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        })
        .done(handleUserAdd)
            .fail(failedAjax);
    }
};

var handleUserAdd = function(json) {
    /* handling the returning data from the server with regards to a user add */ 
    if( json.error ) {
        $( "#row-user" ).addClass("error");
        $( "#user-err" ).removeClass('hidden');
        $( "#user-err" ).html(json.err_msg);
        return 0;
    }

    closeDialog();
    tables['groupMembers'].row.add(json).draw();
};

$( "#addUser button" ).on("click", handleAddUserForm);

</script>
<div class='addUserForm'>

<form id='addUser'>
<div class='instructions'>
Please enter the PennKey of the user you would like to add to this group.
</div>
<div class='fields'>
    <div class="row" id='row-mac'>
        <div class="label">PennKey</div>
        <div class="field"><input name='pennkey' id='pennkey' maxlength=20 size=20></div>
        <div id="user-err" class="hidden"></div>
</div>
<div class="buttons">
<button id='cancel'>Cancel</button><div
class='float-right'><button id='saveadd'> Save &amp; Add</button><button
id='save'>Save</button></div>
</div>
</div>
</div>
