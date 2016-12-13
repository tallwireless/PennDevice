function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
var gid = getCookie('gid');

var readyFunction = function() { 

    registerEvents();

};

var loadContent = function(json) {
    $( "#block" ).unbind();
    $( "#block" ).html("");
    if ( json.error ) {
        displayErrorMessage(json.err_msg);
    }
    $( "#block" ).html(json.content);
    switch (json.resource) {
        case "add_device":
            $( "#block form" ).submit(addDeviceFormProcessing);
            $( "#block .mac" ).focusout(addDeviceMacValidatation);
        break;
    }

}


var failedAjax = function( xhr, status, errorThrown ) {
    alert( "Sorry, there was a problem!" );
    console.log( "Error: " + errorThrown );
    console.log( "Status: " + status );
    console.dir( xhr );
};

function registerEvents() {
    // Handle the buttons in a generic sense
    // The assumation is the id tag of the button will tell the ajax what do
    // fetch
    $( "div.button" ).click(buttonEvent);
    $( "li.tab" ).hover(tabToggle);
    $( "div.device_table div.action a" ).click(deviceAction);

}

var logEvent = function(eventObject) {
    console.log($( this ));
    console.log(eventObject);
};

var deviceAction = function(eventObject) {
    var action = $( this ).attr("id").split("-");
    
    //handling a delete action
    if (action[1] == 'del' || action[1] == 'renew') {
        //for now we are not going to confirm the delete
        $.ajax({
            url: "/ajax/",
            data: {
                func: "updateDevice",
                group_id: gid,
                device: action[0],
                updateAction: action[1]
                },
            type: "POST",
            datatype: "json",
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        })
        .done(handleDeviceUpdate)
        .fail(failedAjax);
        return 0;
    }
};

function displayErrorMessage(msg) {
    $( "#statMsgBox" ).toggleClass('error');
    $( "#statMsgBox" ).slideDown();
    $( "#statMsgBox .title" ).html("ERROR");
    $( "#statMsgBox .message" ).html(msg);
    setTimeout(function () {
        $( "#statMsgBox" ).slideUp();
        $( "#statMsgBox" ).toggleClass('error');
    }, (5*1000));
}

function displaySuccessMessage(msg) {
    $( "#statMsgBox" ).toggleClass('success');
    $( "#statMsgBox" ).slideDown();
    $( "#statMsgBox .title" ).html("SUCCESS");
    $( "#statMsgBox .message" ).html(msg);
    setTimeout(function () {
        $( "#statMsgBox" ).slideUp();
        $( "#statMsgBox" ).toggleClass('success');
    }, (5*1000));
}

var timeoutVar;

var handleDeviceUpdate = function(json) {
    if (json.error) {
        displayErrorMessage(json.err_msg);
        return 0;
    }
    if (json.updateAction == 'del') {
        // we need to remove the line from the table
        var row = $( "#"+json.device );
        displaySuccessMessage("Device "+json.device+" has been suceesfully deleted.");
        row.slideUp();
        row.remove();
    }
    if (json.updateAction == 'renew' ) {
        var expire_cell = $( '#'+json.device+'-expire');
        expire_cell.toggleClass('success');
        expire_cell.html(json.new_expire);
        setTimeout(function() {
            timeoutVar.toggleClass('success');
        }, (1*1000));
    }
}

var buttonEvent = function (eventObject) {
    var id = $( this ).attr("id");
    $.ajax({
        url: "/ajax/",
        data: {
            func: id,
            group_id: gid
            },
        type: "POST",
        datatype: "json",
		beforeSend: function(xhr, settings) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
    })
    .done(loadContent)
    .fail(failedAjax);
};
    

var tabToggle = function (eventObject) {
    $( this ).toggleClass( "highlight" );
}



$(document).ready(readyFunction);
var loadHandlers = function() {
     console.log('lodaing');
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
