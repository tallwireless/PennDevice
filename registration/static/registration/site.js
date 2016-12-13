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
var statMsgBox;

var readyFunction = function() { 
    // Get some helpful variables for later
    
    statMsgBox = $( "#statMsgBox" );

    registerEvents();

};


var loadContent = function(json) {
    if ( json.error ) {
        $( "#block" ).html("Error: "+json.err_msg);
    }
    $( "#block" ).html(json.content);
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

var timeoutVar;

var handleDeviceUpdate = function(json) {
    $( "#block" ).html("<pre>"+JSON.stringify(json, null, 4)+"</pre>");
    if (json.error) {
        console.log("There was an error"+json.err_msg);
        return 0;
    }
    if (json.updateAction == 'del') {
        // we need to remove the line from the table
        var row = $( "#"+json.device );
        row.hide('slide')
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
