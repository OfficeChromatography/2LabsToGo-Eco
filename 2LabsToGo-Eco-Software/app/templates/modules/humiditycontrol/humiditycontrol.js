var isCheckOn = false; 


// Check the state of the sensor when the page loads
$(document).ready(function() {
    if (localStorage.getItem('isCheckOn') === 'true') {
        isCheckOn = true;
    } else {
        isCheckOn = false;
    }

    updateButtonStates();
    
    
}); 

function sendToMachine(value){
    data={'gcode':value}
    $.ajax({
      method: 'POST',
      url:    window.location.origin+'/send/',
      data:   data,
      success: setHommingEndpointSucess,
      error: setHommingEndpointError,
    })
    function setHommingEndpointSucess(data, textStatus, jqXHR){}
    function setHommingEndpointError(jqXHR, textStatus, errorThrown){}
  }
  
  
function updateButtonStates() {
  $('#checkon').attr('disabled', isCheckOn);
  $('#checkoff').attr('disabled', !isCheckOn);
  
  const savedThreshold = localStorage.getItem('threshold');
    if (savedThreshold !== null) {
        $('#thresholdtext').val(savedThreshold); 
        $('#thresholdrange').val(savedThreshold);  
    }
}


$('#thresholdrange').on('change',function(){
$('#thresholdtext').val($(this).val())
})

$('#thresholdtext').on('change',function(){
$('#thresholdrange').val($(this).val())
})

$('#thresholdcontrol').on('click',function(){
    gcode = 'M1100 T'+ $('#thresholdtext').val()
    sendToMachine(gcode)
    localStorage.setItem('threshold', $('#thresholdtext').val());
})

$('#checkon').on('click', function() {
    if (!isCheckOn) {
      var gcode = 'M1100 A1'; 
      sendToMachine(gcode);
      isCheckOn = true;
      localStorage.setItem('isCheckOn', 'true'); 
      $('#checkon').attr('disabled', true);
      $('#checkoff').attr('disabled', false);
    }
  });

  $('#checkoff').on('click', function() {
    if (isCheckOn) {
      var gcode = 'M1100 A0'; 
      sendToMachine(gcode);
      isCheckOn = false;
      localStorage.setItem('isCheckOn', 'false'); 
      $('#checkon').attr('disabled', false);
      $('#checkoff').attr('disabled', true);
    }
  });
