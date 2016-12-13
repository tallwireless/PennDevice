var loadHandlers = function() {
     console.log('lodaing');
     $( "#block form" ).submit(addDeviceFormProcessing);
     $( "#block .mac" ).focusout(addDeviceMacValidatation);
};

var addDeviceMacValidatation = function(eventObject) {
    var usrMac = $( this )[0].value;
    var validMacPatt = /([0-9a-f]:?){6}/i;
    var field = $( this )[0].name.split("-")[1];
    if( ! validMacPatt.test(usrMac) && usrMac != "" ) {
        $( "#row-"+field ).addClass("error");
        $( "#mac-err-"+field ).removeClass('hidden');
    } else {
        $( "#row-"+field ).removeClass("error");
        $( "#mac-err-"+field ).addClass('hidden');
    }
    return false;
};

var addDeviceFormProcessing = function(eventObject) {
    var data = $( this ).serializeArray();
	eventObject.preventDefault();
    $.ajax({
        url: "/ajax/",
        data: {
            func: "add_device",
            group_id: gid,
			data: data
            },
        type: "POST",
        datatype: "json",
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    })
    .done(handleDeviceReturn)
    .fail(failedAjax);
};

var handleDeviceReturn = function(json) {
    var successfulCount = 0;
    var errorCount = 0;
    for ( var index in json.data ) {
        if (json.data.hasOwnProperty(index)) {
            console.log(json.data[index]);
            if ( json.data[index].err ) {
                // display the new error message
                $( "#row-"+index ).addClass("error");
                $( "#mac-err-"+field ).removeClass("hidden");
                $( "#mac-err-"+field ).html(json.data[index].err_msg);
                errorCount += 1;
                continue;
            } else if ( json.data[index].empty ) {
                $( "#row-"+index ).slideUp();
                $( "#row-"+index ).remove();
                continue;
            }

            //we have a successful
            
            // remove the row from the table
            $( "#row-"+index ).slideUp();
            $( "#row-"+index ).remove();

            //update the table
            $.ajax({
                url: "/ajax/",
                data: {
                    func: "get_device",
                    group_id: gid,
                    device: json.data[index].mac
                    },
                type: "POST",
                datatype: "json",
                beforeSend: function(xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            })
            .done(addDeviceToTable)
            .fail(failedAjax);
        }
    }
    console.log("out of the for loop");
    if ( errorCount == 0) {
        $( "#block" ).html("");
    }

};

var addDeviceToTable = function(json) {
    var devTable = $( "#device_table_body" );
    if (json.error) {
        console.log(json.err_msg);
        return false;
    }
    devTable.append("<div class='row' id='"+json.device.mac_address+"'>"+
            "<div class='cell mac'>"+json.device.mac_address+"</div>"+
            "<div class='cell desc'>"+json.device.description+"</div>"+
            "<div class='cell added'>"+json.device.added+"</div>"+
            "<div class='cell expires'>"+json.device.expires+"</div>"+
            "<div class='cell added_by'>"+json.device.added_by+"</div>"+
            "<div class='cell action'><a href=\"javascript:void(0)\" id='"+json.device.mac_address+"-del'>Del</a>"+
            "&nbsp;|&nbsp;<a href=\"javascript:void(0)\" id='"+json.device.mac_address+"-renew'>Renew</a>"+
            "</div>");
    registerEvents();
};
