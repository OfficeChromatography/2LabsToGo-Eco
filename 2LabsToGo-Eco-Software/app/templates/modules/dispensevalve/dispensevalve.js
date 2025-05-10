function sendToMachine(value){
    data={'gcode':value}
    console.log(data);
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

$('#openvalve').on('click',function(){
  sendToMachine('G0X1')         //waste bottle
  sendToMachine('M42P36S255');  //activate 3way-valve 
  sendToMachine('G41'); //open dispensing valve
  sendToMachine('G4S30');    //wait 30 s
  sendToMachine('M42P36S0');  //deactivate 3way-valve 
})
