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

var readyFunction = function() { 
    console.log("The readyFunction has been called");
    registerEvents();
};


var loadContent = function(json) {
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

}

var buttonEvent = function (eventObject) {
    var id = $( this ).attr("id");
    $.ajax({
        url: "/ajax/",
        data: {
            func: id
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
    





$(document).ready(readyFunction);
