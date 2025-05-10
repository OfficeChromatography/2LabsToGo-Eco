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


$("#incuOnButton").on('click',function(e){
  event.preventDefault();
  console.log($("#incu-form").serialize()+'&active=On');
  $.ajax({
  method: 'POST',
  url:    window.location.origin+'/incubationControl/',
  data:   $("#incu-form").serialize()+'&active=On',
  success: staticCleanMethodSuccess,
  error: staticCleanMethodError,
  })
  function staticCleanMethodSuccess(data, textStatus, jqXHR){
  }
  function staticCleanMethodError(jqXHR, textStatus, errorThrown){}
  })

$("#incuOffButton").on('click',function(e){
    gcode1 = 'M104 S0'
    sendToMachine(gcode1)
})

$('#cellincubation').on('click',function(e){
    gcode1 = 'M42I1P24'
    gcode2 = 'M104 S30'
    sendToMachine(gcode1)
    sendToMachine(gcode2)
})

$('#substratincubation').on('click',function(e){
   gcode1 = 'M42I1P24'
   gcode2 = 'M104 S37'
   sendToMachine(gcode1)
   sendToMachine(gcode2)
})

$('#dht22').on('click', function(e){
  gcode1 = 'G99'
  sendToMachine(gcode1)
})
