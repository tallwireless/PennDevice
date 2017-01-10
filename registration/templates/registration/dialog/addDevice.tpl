<script>
var handleAddDeviceForm = function (eventObj) {
    eventObj.preventDefault();
    var button = $(this).attr('id');
    if( button == 'cancel') {
        closeDialog();
    }
    if( button == 'saveadd' || button == 'save') {
        /* Let's collect the form data and see what's up with it */

        /* First the MAC address
         *
         * This is a required field that must be in the format of
         * 'aa:bb:cc:dd:ee:ff'. If it isn't, then we need to let the user know
         * so that they can fix it.
         */
        var mac = $( "#mac" )[0].value;
        var des = $( "#des" )[0].value;
        var validMacPatt = /([0-9a-f]{2}:){5}[0-9a-f]{2}/i;
        console.log(mac);
        if( ! validMacPatt.test(mac) ) {
            $( "#row-mac" ).addClass("error");
            $( "#mac-err" ).removeClass('hidden');
            $( "#mac-err" ).html("Please provide a valid MAC address.");
            return 0;
        } else {
            $( "#row-mac" ).removeClass("error");
            $( "#mac-err" ).addClass('hidden');
        } 
        /* 
         * Now that we have a valid MAC address, let's send it off to the API
         * to be added to the group.
         */

        $.ajax({
            url: "/api/groups/"+getCurrentGroup()+"/devices/"+mac+"?table",
            type: "PUT",
            data: JSON.stringify({ des: des }),
            datatype: "json",
            processData: false,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        })
        .done(handleDeviceAdd)
            .fail(failedAjax);
    }
};

var handleDeviceAdd = function(json) {
    /* This function handles the return data from the API call to add a device
     * to a group, and then take approriate action.*/
    if(json.error) {
        $( "#row-mac" ).addClass("error");
        $( "#mac-err" ).removeClass('hidden');
        $( "#mac-err" ).html(json.err_msg);
        return 0;
    }

    closeDialog();
    tables['device'].row.add(json).draw();
};

$( "#addDevice button" ).on("click", handleAddDeviceForm);

</script>
<div class='addDeviceForm'>
<form id='addDevice'>
<div class='fields'>
    <div class="row" id='row-mac'>
        <div class="label">MAC Address</div>
        <div class="field"><input name='mac' id='mac' maxlength=17 size=17></div>
        <div id="mac-err" class="hidden"></div>
    <div class="row" id='row-desc'>
        <div class="label">Description</div>
        <div class="field"><input name="des" id='des' maxlength=254 size=30></div>
    </div>
</div>
<div class="buttons">
<button id='cancel'>Cancel</button><div
class='float-right'><button id='saveadd'> Save &amp; Add</button><button
id='save'>Save</button></div>
</div>
</div>
</div>
