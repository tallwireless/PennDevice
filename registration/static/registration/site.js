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
    loadHandlers = function() { return false; }; 
    if ( json.error ) {
        displayErrorMessage(json.err_msg);
    }
    $( "#block" ).html(json.content);
    loadHandlers();
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
