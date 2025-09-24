var isCheckOnUp = false; 
var isCheckOnDown = false; 


// Check the state of the sensor when the page loads
$(document).ready(function() {
//    if (localStorage.getItem('isCheckOnUp') === 'true') {
//        isCheckOnUp = true;
//    } else {
//        isCheckOnUp = false = false;
//    }
//});
    
//$(document).ready(function() {
//    if (localStorage.getItem('isCheckOnDown') === 'true') {
//        isCheckOnDown = true;
//    } else {
//        isCheckOnDown = false;
//    }
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
  $('#checkondown').attr('disabled', isCheckOnDown);
  $('#checkoffdown').attr('disabled', !isCheckOnDown);
  $('#checkonup').attr('disabled', isCheckOnUp);
  $('#checkoffup').attr('disabled', !isCheckOnUp);
  
  const savedThresholdDown = localStorage.getItem('thresholddown');
    if (savedThresholdDown !== null) {
        $('#thresholdtextdown').val(savedThresholdDown); 
        $('#thresholdrangedown').val(savedThresholdDown);
    }
  const savedThresholdUp = localStorage.getItem('thresholdup');
    if (savedThresholdUp !== null) {
        $('#thresholdtextup').val(savedThresholdUp); 
        $('#thresholdrangeup').val(savedThresholdUp);  		
    }
}


$('#thresholdrangedown').on('change',function(){
$('#thresholdtextdown').val($(this).val())
})

$('#thresholdrangeup').on('change',function(){
$('#thresholdtextup').val($(this).val())
})

//$('#thresholdtext').on('change',function(){
//$('#thresholdrange').val($(this).val())
//})

$('#thresholdcontroldown').on('click',function(){
    gcode = 'M1100 T'+ $('#thresholdtextdown').val()
    sendToMachine(gcode)
    localStorage.setItem('thresholddown', $('#thresholdtextdown').val());
})

$('#thresholdcontrolup').on('click',function(){
    gcode = 'M1200 T'+ $('#thresholdtextup').val()
    sendToMachine(gcode)
    localStorage.setItem('thresholdup', $('#thresholdtextup').val());
})

$('#checkondown').on('click', function() {
    if (!isCheckOnDown) {
      var gcode = 'M1100 A1'; 
      sendToMachine(gcode);
      isCheckOnDown = true;
      localStorage.setItem('isCheckOnDown', 'true'); 
      $('#checkondown').attr('disabled', true);
      $('#checkoffdown').attr('disabled', false);
    }
  });

  $('#checkoffdown').on('click', function() {
    if (isCheckOnDown) {
      var gcode = 'M1100 A0'; 
      sendToMachine(gcode);
      isCheckOnDown = false;
      localStorage.setItem('isCheckOnDown', 'false'); 
      $('#checkondown').attr('disabled', false);
      $('#checkoffdown').attr('disabled', true);
    }
  });
  
  $('#checkonup').on('click', function() {
    if (!isCheckOnUp) {
      var gcode = 'M1200 A1'; 
      sendToMachine(gcode);
      isCheckOnUp = true;
      localStorage.setItem('isCheckOnUp', 'true'); 
      $('#checkonup').attr('disabled', true);
      $('#checkoffup').attr('disabled', false);
    }
  });

  $('#checkoffup').on('click', function() {
    if (isCheckOnUp) {
      var gcode = 'M1200 A0'; 
      sendToMachine(gcode);
      isCheckOnUp = false;
      localStorage.setItem('isCheckOnUp', 'false'); 
      $('#checkonup').attr('disabled', false);
      $('#checkoffup').attr('disabled', true);
    }
  });
