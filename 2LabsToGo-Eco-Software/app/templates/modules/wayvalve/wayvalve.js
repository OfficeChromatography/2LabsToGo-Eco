$("#valvecontrol").on('click',function(e){
    e.preventDefault();
    console.log($("#wayvalveControlForm").serialize());
    $.ajax({
    method: 'POST',
    url:    window.location.origin+'/wayvalve/',
    data:   $("#wayvalveControlForm").serialize(),
    success: staticCleanMethodSuccess,
    error: staticCleanMethodError,
    })
    function staticCleanMethodSuccess(data, textStatus, jqXHR){
    }
    function staticCleanMethodError(jqXHR, textStatus, errorThrown){}
})

$('#valveRange').on('change',function(){
  $('#valveCycles').val($(this).val())
})
$('#valveCycles').on('change',function(){
  $('#valveRange').val($(this).val())
})

$('#valvecontrol').on('click',function(){
  s = $('#valveCycles').val()
  for (let i = 0; i < s; i++) {
  sendToMachine('M42P36S255'); //activate valve
  sendToMachine('G4S1');    //wait 1 s
  sendToMachine('M42P36S0');   //deactivate valve
  sendToMachine('G4S1');    //wait 1 s
  }
})

