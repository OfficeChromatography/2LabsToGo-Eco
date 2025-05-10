document.addEventListener("DOMContentLoaded", function() {
  var isLightOn = false; // Track the state of the light

  function sendToMachine(value) {
    var data = {'gcode': value};
    console.log(data);
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

  $('#lightrange').on('change',function(){
    $('#inttext').val($(this).val())
  })
  $('#inttext').on('change',function(){
    $('#lightrange').val($(this).val())
  })

  $('#lighton').on('click', function() {
    if (!isLightOn) {
      var gcode = 'M355 S1 P'+ $('#inttext').val(); 
      sendToMachine(gcode);
      isLightOn = true;
      $('#lighton').attr('disabled', true);
      $('#lightoff').attr('disabled', false);
    }
  });

  $('#lightoff').on('click', function() {
    if (isLightOn) {
      var gcode = 'M355 S0 P'+ $('#inttext').val(); 
      sendToMachine(gcode);
      isLightOn = false;
      $('#lighton').attr('disabled', false);
      $('#lightoff').attr('disabled', true);
    }
  });
});


