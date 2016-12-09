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
    console.log(id);
    console.log(className);
    var obj = document.getElementById(id);
    console.log(obj);
    if ( obj.className == "hidden") {
        console.log("the object is hidden");
        obj.className = className;
    } 
    else {
        console.log("the object is not hidden");
        obj.className = "hidden";
    }
}


