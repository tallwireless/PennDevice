/*Admin Page Java Script*/

var readyFunction = function() {
    registerEvents();
};

function registerEvents() {
    $( "li.tab" ).hover(tabToggle).click(tabClick);
}

var tabToggle = function (eventObject) {
        $( this ).toggleClass( "highlight" );
}

var tabClick = function (eventObject) {
    var id = $(this).attr('id');
    console.log("You clicked on the \'"+id+"\' button");
};

$(document).ready(readyFunction);

var buttonEvent = function (eventObject) {
    var id = $( this ).attr("id");
    $.ajax({
        url: "/ajax/",
        data: {
            func: 'admin',
            page: id,
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

var loadContent = function(json) {
    $( "#page_block" ).unbind();
    $( "#page_block" ).html("");
    if ( json.error ) {
        disPageErrMsg(json.err_msg);
    }
    $( "#page_block" ).html(json.content);
    switch (json.resource) {
    }

}
