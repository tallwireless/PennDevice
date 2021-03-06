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
    $( "#dialog" ).dialog({autoOpen:false, "modal": true} );

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
            $( "div#add_devices_form" ).on("click",handleAddDeviceFormClick);
            $( "div#add_user_form" ).on("click",handleAddUserFormClick);
            break;
    }
}

var handleAddUserFormClick = function (eventobj) {
    fetchDialogBox('addUser','Add User');
};

var handleAddDeviceFormClick = function (eventobj) {
    fetchDialogBox('addDevice','Add Device');
};

var fetchDialogBox = function(page,title) {
    $.ajax({
        url: "/ajax/",
        data: {
            func: 'dialogPage',
            page: page,
            title: title
        },
        type: "POST",
        datatype: "json",
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    })
    .done(loadDialogBox)
        .fail(failedAjax);
};

var loadDialogBox = function (json) {
    if (json.error) {
        console.log(json);
        alert("there was an error.");
    }
    /* load content into the dialog box first */
    $( "#dialog" ).html(json.html);
    $( "#dialog" ).dialog("option", "title", json.title);
    $( "#dialog" ).dialog("option", "width", "550px");

    /* now let's open the dialog box */
    $( "#dialog" ).dialog("open");
};

function closeDialog() {
    $( "#dialog" ).dialog("close");
    $( "#dialog" ).html("");
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
            'data': 'admin',
            'title': 'Admin',
            'class': 'admin',
            'render': function(data, type, full, meta) {
                if (data == true) {
                    return "<a href='javascript:void(0)' id='adminYes-" + full.username + "'>Yes</a>";
                } else {
                    return "<a href='javascript:void(0)' id='adminNo-" + full.username + "'>No</a>";
                }
            }
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
    var user = $( this )[0].id.split("-")[1];
    var action = "DELETE"; 
    $.ajax({
        url: "/api/groups/"+getCurrentGroup()+"/members/"+user,
        type: action,
        datatype: "json",
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    })
    .done(handleGroupMemberDelete)
        .fail(failedAjax);
};

var handleGroupMemberDelete = function(json) {
    if ( json.error ) {
        disBlockErrMsg(json.err_msg);
        return 0;
    }
    var row = tables['groupMembers'].row( "#"+json.username );
    var data = row.data();
    row.remove().draw( false );
};

var handleGroupAdminEvent = function(eventOject) {
    var state = $( this )[0].id.split("-")[0];
    var user = $( this )[0].id.split("-")[1];
    var action = "PATCH"; 
    var foobar = {};
    foobar['username']=user;
    if (state == 'adminYes') {
        foobar['admin'] = false;
    } else if (state == 'adminNo') {
        foobar['admin'] = true;
    }
    //for now we are not going to confirm the delete
    $.ajax({
        url: "/api/groups/"+getCurrentGroup()+"/members/",
        data: JSON.stringify([ foobar ]),
        type: action,
        datatype: "json",
        processData: false,
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    })
    .done(handleGroupAdminUpdate)
        .fail(failedAjax);
};

var handleGroupAdminUpdate = function(json) {
    if ( json[0].error ) {
        disBlockErrMsg(json.err_msg);
        return 0;
    }
    var user = json[0].username;
    var admin = json[0].admin;
    var row = tables['groupMembers'].row( "#"+user );
    var data = row.data();
    data['admin'] = admin;
    row.data(data).draw();
};

var groupMemberCreateRow = function( a, b, c ) {
    $(a).on("click",".admin a",handleGroupAdminEvent);
    $(a).on("click",".action a",handleGroupMemberEvent);
};

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
