var alert_showing =  false;

$('#newbttn').on('click', function (e) {
  e.preventDefault()
  editor.setValue('');
  $('#filename').val('');

})

$('#savebttn').on('click', function (e) {
  e.preventDefault()
  text = editor.getValue();
  $endpoint = window.location.origin+'/gcode-editor/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   '&SAVE&text='+text+'&name='+$('#filename').val(),
  success: savefileMethodSuccess,
  error: savefileMethodError,
  })
})

$('#list-load').on('click','#list-home-list', function (e) {
e.preventDefault()
data={'filename':$(this)[0].innerHTML, 'LOADFILE':''}
$.ajax({
  method: 'GET',
  url:    window.location.origin+'/gcode-editor/',
  data:   data,
  success: loadfileMethodSuccess,
  error: loadfileMethodError,
})
})

$('#startbttn').on('click', function (e) {
  e.preventDefault()
  data =
  $endpoint = window.location.origin+'/gcode-editor/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   '&START&name='+$('#filename').val(),
  success: startFileMethodSuccess,
  error: startFileMethodError,
  })
})

$('#stopbttn').on('click', function (e) {
  e.preventDefault()
  $endpoint = window.location.origin+'/gcode-editor/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   '&STOP',
  success: stopExecMethodSuccess,
  error: stopExecMethodError,
  })
})

$('#removebttn').on('click', function (e) {
  e.preventDefault()
  $endpoint = window.location.origin+'/gcode-editor/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   '&REMOVE&name='+$('#filename').val(),
  success: removeFileMethodSuccess,
  error: removeFileMethodError,
  })
})

$('#removefilebttn').on('click', function (e) {
  $('#file').next('.custom-file-label').html('');
  $('#file').val('')
  $('#sizesfile').html('')
})

$("#uploadbttn").on('click' ,function() {
    var fd = new FormData();
    fd.append('UPLOAD','');
    var files = $('#file')[0].files[0];
    fd.append('file', files);
    $.ajax({
        method: 'POST',
        url: window.location.origin+'/gcode-editor/',
        data: fd,
        contentType: false,
        processData: false,
        success: uploadfileMethodSuccess,
        error: uploadfileMethodError,
    });
});


$('#file').on('change',function(e){
                var fileName = e.target.files[0];
                $('#sizesfile').html('Size: '+ Math.round(fileName.size/1000) + ' Kbytes')
                $(this).next('.custom-file-label').html(fileName.name);
            })

function uploadfileMethodSuccess(data, textStatus, jqXHR){
  alertManager(data)
  loadlistofgcodes()
}
function uploadfileMethodError(jqXHR, textStatus, errorThrown){}
function loadfileMethodSuccess(data, textStatus, jqXHR){
  editor.setValue(data.text);
  $('#filename').val(data.filename)
  alertManager(data)
}
function loadfileMethodError(jqXHR, textStatus, errorThrown){}
function savefileMethodSuccess(data, textStatus, jqXHR){
  alertManager(data)
  loadlistofgcodes()
}
function savefileMethodError(jqXHR, textStatus, errorThrown){}
function startFileMethodSuccess(data, textStatus, jqXHR){
  alertManager(data)
}
function startFileMethodError(jqXHR, textStatus, errorThrown){}
function stopExecMethodSuccess(data, textStatus, jqXHR){
  alertManager(data)
}
function stopExecMethodError(jqXHR, textStatus, errorThrown){}
function removeFileMethodSuccess(data, textStatus, jqXHR){
  alertManager(data)
  loadlistofgcodes()
}
function removeFileMethodError(jqXHR, textStatus, errorThrown){}
function alertManager(data){
  if (data.primary){
    alertAnimation('primary',data.primary)
  }
  if (data.secondary){
    alertAnimation('secondary',data.secondary)
  }
  if (data.success){
    alertAnimation('success',data.success)
  }
  if (data.danger){
    alertAnimation('danger',data.danger)
  }
  if (data.warning){
    alertAnimation('warning',data.warning)
  }
  if (data.info){
    alertAnimation('info',data.info)
  }
  if (data.light){
    alertAnimation('light',data.light)
  }
  if (data.dark){
    alertAnimation('dark',data.dark)
  }
}
function alertAnimation(typeofalert,message){
  if (alert_showing==false){
    alert_showing = true
    $('#alert').addClass('alert-'+typeofalert).html(message)
    $('#alert').fadeIn().delay(800).fadeOut(400, function(){$('#alert').removeClass('alert-'+typeofalert)});
    alert_showing = false
  }
}
function loadlistofgcodes(){
  $.ajax({
    method: 'GET',
    url:    window.location.origin+'/gcode-editor/',
    data:   '&LISTLOAD',
    success: loadlistMethodSuccess,
    error: loadlistMethodError,
  })
  function loadlistMethodSuccess(data, textStatus, jqXHR){
    $('#list-load').empty()
    $.each(data, function(key, value) {
        $('#list-load').append('<a class="list-group-item list-group-item-action py-1" id="list-home-list" data-toggle="list" href="#list-home" role="tab" aria-controls="home">'+value+'</a>')
      })
    return
  }
  function loadlistMethodError(jqXHR, textStatus, errorThrown){}
}
