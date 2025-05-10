document.addEventListener("DOMContentLoaded", function() {
    var isLightOn = false; // Track the state of the light
  
    function sendToMachine(value) {
      var data = {'gcode': value};
      $.ajax({
        method: 'POST',
        url: window.location.origin + '/send/',
        data: data,
        success: setHommingEndpointSucess,
        error: setHommingEndpointError,
      });
    }
  
    function setHommingEndpointSucess(data, textStatus, jqXHR) {
      console.log("Success!");
    }
  
    function setHommingEndpointError(jqXHR, textStatus, errorThrown) {
      console.log(errorThrown);
    }
  
    $('#lighton').on('click', function() {
      if (!isLightOn) {
        var gcode = 'M42 P13 S255'; 
        sendToMachine(gcode);
        isLightOn = true;
        $('#lighton').attr('disabled', true);
        $('#lightoff').attr('disabled', false);
      }
    });
  
    $('#lightoff').on('click', function() {
      if (isLightOn) {
        var gcode = 'M42 P13 S0'; 
        sendToMachine(gcode);
        isLightOn = false;
        $('#lighton').attr('disabled', false);
        $('#lightoff').attr('disabled', true);
      }
    });
  });
  