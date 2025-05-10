let timeout;

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

$('#intensityrange').on('change',function(){
  $('#intensitytext').val($(this).val())
})
$('#intensitytext').on('change',function(){
  $('#intensityrange').val($(this).val())
})

$('#turnoff').on('click',function(){
  gcode = 'M42P3S0'
  sendToMachine(gcode)
  if (timeout) {
    clearTimeout(timeout);
    timeout = null;
  }
})



function showAlert() {
  if (confirm("Switch off the nebulizer!!")) {
    
    executeCommand();
  } else {
   
  }
}

function executeCommand() {
      gcode = 'M42P3S0'
      sendToMachine(gcode);
      if (timeout) {
        clearTimeout(timeout);
        timeout = null;
      }
  
  console.log("The nebulizer is now switched off.");
}

$('#manualcontrol').on('click',function(){
      gcode = 'M42P3S'+ $('#intensitytext').val()
      sendToMachine(gcode);
      if (!timeout) {
        timeout = setTimeout(showAlert, 120000);
      }
})



$('#s50').on('click', function () {
  gcode = 'M42P3S50'; 
  sendToMachine(gcode);
  if (!timeout) {
    timeout = setTimeout(showAlert, 120000);
  } 
});

$('#s200').on('click', function () {
  gcode = 'M42P3S200'; 
  sendToMachine(gcode);
  if (!timeout) {
    timeout = setTimeout(showAlert, 120000);
  }
});

