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

var failedAjax = function( xhr, status, errorThrown ) {
    alert( "Sorry, there was a problem!" );
    console.log( "Error: " + errorThrown );
    console.log( "Status: " + status );
    console.dir( xhr );
};


var logEvent = function(eventObject) {
    console.log($( this ));
    console.log(eventObject);
};

function disPageErrMsg(msg) {
    disErrMsgBox("#statMsgBox",msg);
}
var errTimeout;

function disErrMsgBox(id,msg) {
    errTimeout = id;
    $( id ).toggleClass('error');
    $( id ).slideDown();
    $( id+" .title" ).html("ERROR");
    $( id+" .message" ).html(msg);
    setTimeout(function () {
        $( errTimeout ).slideUp();
        $( errTimeout ).toggleClass('error');
    }, (5*1000));
}

function disPageSucMsgBox(msg) {
    disSucMsgBox("#statMsgBox",msg);
}
var sucTimeout;
function disSucMsgBox(id,msg) {
    sucTimeout = id;
    $( id ).toggleClass('success');
    $( id ).slideDown();
    $( id+" .title" ).html("SUCCESS");
    $( id+" .message" ).html(msg);
    setTimeout(function () {
        $( sucTimeout ).slideUp();
        $( sucTimeout ).toggleClass('success');
    }, (2*1000));
}

var tabToggle = function (eventObject) {
    $( this ).toggleClass( "highlight" );
}

$(document).ready(readyFunction);

