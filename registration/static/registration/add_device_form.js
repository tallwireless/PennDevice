var loadHandlers = function() {
     console.log('lodaing');
     $( "#block form" ).submit(addDeviceFormProcessing);
     $( "#block .mac" ).focusout(addDeviceMacValidatation);
};

var addDeviceMacValidatation = function(eventObject) {
    console.log("validate");
};

var addDeviceFormProcessing = function(eventObject) {
    console.log("form");
};
