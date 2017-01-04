/*Admin Page Java Script*/

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
var tables = [];

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

var sucTimeout;
function disSucMsgBox(msg) {
    id = "#statMsgBox";
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

var readyFunction = function() {
    console.log("Starting...");
    registerEvents();
    fetchContent('groups');

};

$(document).ready(readyFunction);

function registerEvents() {
    $( "li.tab" ).hover(tabToggle).click(tabClick);
}

var tabToggle = function (eventObject) {
        $( this ).toggleClass( "highlight" );
}

var fetchContent = function (page) {
    $.ajax({
        url: "/ajax/",
        data: {
            func: 'admin',
            page: page,
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

var tabClick = function (eventObject) {
    var id = $(this).attr('id');
    fetchContent(id);
};

var loadContent = function(json) {
    $( "#page_block" ).unbind();
    $( "#page_block" ).html("");
    if ( json.error ) {
        disPageErrMsg(json.err_msg);
    }
    $( "#page_block" ).html(json.content);
    /* Un-highlight-current tab */
    $( 'li.selected' ).toggleClass('selected');
    $( '#'+json.page ).toggleClass('selected');
    switch( json.page ) {
        case 'groups':
            $( "select#group" ).change(loadGroupInformation);
            loadGroupInformation();
            break;
    }
}

function adminUpdateSubtitle(newTitle) { 
    $( "span.subtitle" ).html("Administration - "+newTitle);
}

var getCurrentGroup = function () {
    return $( "select#group option:selected" ).attr('value');
}

var getCurrentGroupName = function() {
    return $( "select#group option:selected" ).text();
}

var loadGroupInformation = function (eventObject) {
    console.log($(this));
    adminUpdateSubtitle("Group "+getCurrentGroupName());
    loadGroupDeviceTable();
    loadGroupUserTable();
};

var deviceTableNewRow = function(row, data, dataIndex) {
    $(row).on("click","a",handleDeviceEvent);
};

var handleDeviceEvent = function(eventObject) {
    var action = $( this )[0].id.split("-");

    if (action[0] == 'del') { 
        //for now we are not going to confirm the delete
        $.ajax({
            url: "/api/devices/"+action[1]+"/?ui",
            type: "DELETE",
            datatype: "json",
            beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);}
        })
        .done(handleDeviceDelete)
        .fail(failedAjax);
    }
    if (action[0] == 'renew') {
        //for now we are not going to confirm the delete
        $.ajax({
            url: "/api/devices/"+action[1]+"/?ui",
            type: "PATCH",
			data: {"expires": "2020-12-01T23:17:30Z"},
            datatype: "json",
            beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);}
        })
        .done(handleDeviceRenew)
        .fail(failedAjax);
    }
};

var handleDeviceDelete = function(json) {
    if (json.error) {
        disPageErrMsg(json.err_msg);
        return 0;
    }
	tables['device'].row( "#"+json.device ).remove().draw( false );
	disSucMsgBox("Device "+json.device+" has been suceesfully deleted.");
};

var handleDeviceRenew = function(json) {
    if (json.error) {
        disPageErrMsg(json.err_msg);
        return 0;
    }
	var expire_cell = $( '#'+json.device+'-expire');
	expire_cell.toggleClass('success');
	expire_cell.html(json.expires);
	setTimeout(function() {
		timeoutVar.toggleClass('success');
	}, (1*1000));
};


function loadGroupDeviceTable() {
    if ('device' in tables) {
        tables['device'].destroy();
    }

    tables['device'] = $( "#deviceTable" ).DataTable( {
       "language": { 'emptyTable': "There are no MAC addresses registered to this group." },
       "processing" : true,
       //"serverSide" : true,
       "paging"     : false,
       "createdRow" : deviceTableNewRow,
       "ajax"       : {
                    url: "/api/groups/"+getCurrentGroup()+"/devices?table",
                    type: "GET",
                    datatype: "json",
                },
        "columns": [
            {
                'data': 'mac_address',
                'title': "MAC Address",
                'class': 'mac',
                'type': 'num'
            }, {
                'data': 'description',
                'title': "Description",
                'class': 'desc'
            }, {
                'data': 'added',
                'title': 'Added On',
                'class': 'added',
                'type': 'date'
            }, {
                'data': 'expires',
                'title': 'Expires On',
                'class': 'expires',
                'type': 'date'
            }, {
                'data': 'added_by',
                'title': 'Added By',
                'class': 'added_by'
            }, {
                'data': 'action',
                'title': 'Action',
                'class': 'action',
                'defaultContent': "",
                "render": function(data, type, full, meta) {
                    return "<a href='javascript:void(0)' id='del-"+full.mac_address+"'>Del</a> | "+
                           "<a href='javascript:void(0)' id='renew-"+full.mac_address+"'>Renew</a}";
                }
            }
       ]});
}

function loadGroupUserTable() {
   if ('groupMembers' in tables) {
       tables['groupMembers'].destroy();
    }
   tables['groupMembers'] = $( "#membersTable" ).DataTable( {
       "language": { 'emptyTable': "There are no members in this group." },
       "createdRow" : groupMemberCreateRow,
       "processing" : true,
       "paging"     : false,
       "ajax"       : {
                    url: "/api/groups/"+getCurrentGroup()+"/members?table",
                    type: "GET",
                    datatype: "json",
                },
        "order": [[1, 'asc']],
        "columns": [ 
            {
                'data': 'first_name',
                'title': 'First Name',
                'class': 'name'
            }, {
                'data': 'last_name',
                'title': 'Last Name',
                'class': 'name'
            }, {
                'data': 'username',
                'title': 'PennKey',
                'class': 'pennkey'
            }, {
                'data': 'action',
                'title': 'Action',
                'class': 'action',
                'defaultContent': '',
                'render': function(data, type, full, meta) {
                    return "<a href='javascript:void(0)' id='del-" + full.username + "'>Del</a>";
                }
            }
        ]});
}

var handleGroupMemberEvent = function(eventOject) {
    var action = $( this )[0].id.split("-");
    
    //handling a delete action
    if (action[0] == 'toggle' || action[0] == 'del') {
        //for now we are not going to confirm the delete
        $.ajax({
            url: "/ajax/",
            data: {
                func: "updateGroupMember",
                group_id: gid,
                user: action[1],
                updateAction: action[0]
                },
            type: "POST",
            datatype: "json",
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        })
        .done(handleGroupMemberUpdate)
        .fail(failedAjax);
        return 0;
    }
};

var handleGroupMemberUpdate = function(json) {
    if ( json.error ) {
        disBlockErrMsg(json.err_msg);
        return 0;
    }
    var row = tables['groupMembers'].row( "#"+json.user );
    var data=row.data();
    switch(json.action) {
        case "del":
            row.remove().draw( false );
            disBlockSucMsg(json.sucMsg);
            break;
        case "toggle":
            data['admin']=json.admin;
            row.data(data).draw();
            if (json.sucMsg) {
                disBlockSucMsg(json.sucMsg);
            }
            break;
        case "addMember":
            var memberdata = json.member;
            tables['groupMembers'].row.add(memberdata).draw();
            disBlockSucMsg(json.sucMsg);
            $( "#newUser").val("");
            break;

    }
};

var groupMemberCreateRow = function( a, b, c ) {
    $(a).on("click","a",handleGroupMemberEvent);
};

