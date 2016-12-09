function validateMac(field) {
    var usrMac = document.getElementById("mac-"+field).value;
    var validMacPatt = /([0-9a-f]:?){6}/i;
    if ( validMacPatt.test(usrMac) || usrMac == "" ) {
        document.getElementById("row-"+field).className = "device_table_row";
        document.getElementById("mac-err-"+field).className = "hidden";
        return true;
    }
    else {

        document.getElementById("row-"+field).className += " error";
        document.getElementById("mac-err-"+field).className = "form_error_message";
        document.getElementById("mac-"+field).focus();
        return false;
    }
    
    return true;
}


function showBlock(id,className) {
    var obj = document.getElementById(id);
    if ( obj.className == "hidden") {
        obj.className = className;
    } 
    else {
        obj.className = "hidden";
    }
}

function highlight(id) {
    var obj = document.getElementById(id);
    if ( obj.className == "highlight") {
        obj.className = "other-group";
    } 
    else {
        obj.className = "highlight";
    }
}


