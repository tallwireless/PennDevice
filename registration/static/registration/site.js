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
var tables = {};
var readyFunction = function() { 

    displayDeviceTable();
    registerEvents();

};

var loadContent = function(json) {
    $( "#block" ).unbind();
    $( "#block" ).html("");
    if ( json.error ) {
        disPageErrMsg(json.err_msg);
    }
    $( "#block" ).html(json.content);
    switch (json.resource) {
        case "add_device":
            $( "#block form" ).submit(addDeviceFormProcessing);
            $( "#block .mac" ).focusout(addDeviceMacValidatation);
            break;
        case "admin_group":
            displayGroupMemberTable();
            setupAddUser();
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
}

var logEvent = function(eventObject) {
    console.log($( this ));
    console.log(eventObject);
};

var handleDeviceEvent = function(eventObject) {
    var action = $( this )[0].id.split("-");
    
    //handling a delete action
    if (action[0] == 'del' || action[0] == 'renew') {
        //for now we are not going to confirm the delete
        $.ajax({
            url: "/ajax/",
            data: {
                func: "updateDevice",
                group_id: gid,
                device: action[1],
                updateAction: action[0]
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


function disBlockErrMsg(msg) {
    disErrMsgBox("#statMsgBoxBlock",msg);
}
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

function disBlockSucMsg(msg) {
    disSucMsgBox("#statMsgBoxBlock",msg);
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

var handleDeviceUpdate = function(json) {
    if (json.error) {
        disPageErrMsg(json.err_msg);
        return 0;
    }
    if (json.updateAction == 'del') {
        // we need to remove the line from the table
        tables['device'].row( "#"+json.device ).remove().draw( false );
        disPagSucMsg("Device "+json.device+" has been suceesfully deleted.");
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
    if ( errorCount == 0) {
        $( "#block" ).html("");
    }

};

var addDeviceToTable = function(json) {
    if (json.error) {
        return false;
    }
    json.device.DT_RowId = json.device.mac_address;
    tables['device'].row.add(json.device).draw();
};

var deviceTableNewRow = function(row, data, dataIndex) {
    $(row).on("click","a",handleDeviceEvent);
};

var displayDeviceTable = function() {
   tables['device'] = $( "#deviceTable" ).DataTable( {
       "language": { 'emptyTable': "There are no MAC addresses registered to this group." },
       "processing" : true,
       //"serverSide" : true,
       "paging"     : false,
       "createdRow" : deviceTableNewRow,
       "ajax"       : {
                    url: "/ajax/",
                    data: {
                        func: "get_group_device_table",
                        group_id: gid,
                    },
                    type: "POST",
                    datatype: "json",
                    beforeSend: function(xhr, settings) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
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
};


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

var displayGroupMemberTable = function() {
   tables['groupMembers'] = $( "#groupMembers" ).DataTable( {
       "language": { 'emptyTable': "There are no members in this group." },
       "createdRow" : groupMemberCreateRow,
       "processing" : true,
       //"serverSide" : true,
       "paging"     : false,
       "ajax"       : {
                    url: "/ajax/",
                    data: {
                        func: "get_group_members_table",
                        group_id: gid,
                    },
                    type: "POST",
                    datatype: "json",
                    beforeSend: function(xhr, settings) {
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                },
        "order": [[1, 'asc']],
        "columns": [ 
			{
				'data': 'fname',
				'title': 'First Name',
				'class': 'name'
			}, {
				'data': 'lname',
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
					return "<a href='javascript:void(0)' id='toggle-" + full.username + "'>" + data + "</a>";
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
};


var setupAddUser = function() {
    $( "#add-members" ).submit(handleAddUserSubmit);
    $( "#newUser" ).focusout(handleAddUserValidation);
}

var handleAddUserSubmit = function(eventObject) {
    eventObject.preventDefault();
    var data = $( this ).serializeArray();
     
    if (data[0]['value'] == ""){
        disBlockErrMsg("You need to provide a PennKey");
        return 0;
    }

    $.ajax({
        url: "/ajax/",
        data: {
            func: "updateGroupMember",
            updateAction: "addMember",
            group_id: gid,
			user: data[0]['value']
            },
        type: "POST",
        datatype: "json",
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    })
    .done(handleGroupMemberUpdate)
    .fail(failedAjax);
    
}

var handleAddUserValidation = function(eventObject) {
    var value = $( this ).val();
    if (value == "" ) {
        disBlockErrMsg("You need to provide a PennKey");
        return;
    }
}
