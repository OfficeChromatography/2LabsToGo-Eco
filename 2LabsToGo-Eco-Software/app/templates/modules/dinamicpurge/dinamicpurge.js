
// Cleaning EndPoint
$('#cleanbttn').on('click', function (e) {
  event.preventDefault()
  $formData = 'PROCESS&'+$('#cleaningprocessform').serialize()
  $endpoint = window.location.origin+'/cleanprocess/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: cleanMethodSuccess,
  error: cleanMethodError,
  })
})
$('#stopbttn').on('click', function (e) {
  event.preventDefault()
  //
  $formData = 'STOP&'
  $endpoint = window.location.origin+'/cleanprocess/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: stopMethodSuccess,
  error: stopMethodError,
  })
})
$('#pausebttn').on('click', function (e) {
  event.preventDefault()
  //
  $formData = 'PAUSE&'
  $endpoint = window.location.origin+'/cleanprocess/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: pauseMethodSuccess,
  error: pauseMethodError,
  })
})


function cleanMethodSuccess(data, textStatus, jqXHR){
  $('.control-bttn').removeClass('btn-danger btn-secondary')
  $('.control-bttn').addClass('btn btn-success')
  cleaningstatusalert(true, data.message)
  checkStatusInterval = setInterval("checkCleaningStatus()", 3000);
}
function cleanMethodError(jqXHR, textStatus, errorThrown){
  console.log(errorThrown)
}
function stopMethodSuccess(data, textStatus, jqXHR){
  $('.control-bttn').removeClass('btn-success btn-secondary')
  $('.control-bttn').addClass('btn btn-danger')
}
function stopMethodError(jqXHR, textStatus, errorThrown){}
function pauseMethodSuccess(data, textStatus, jqXHR){
    $('.control-bttn').removeClass('btn-success btn-danger')
  $('.control-bttn').addClass('btn btn-secondary')
}
function pauseMethodError(jqXHR, textStatus, errorThrown){}


// Cleaning status EndPoint
var checkStatusInterval
function checkCleaningStatus(){
  $formData = 'checkstatus'
  $endpoint = window.location.origin+'/cleanprocess/'
  $.ajax({
  method: 'GET',
  url:    $endpoint,
  data:   $formData,
  success: checkCleaningSuccess,
  error: checkCleaningError,
  })

  function checkCleaningSuccess(data, textStatus, jqXHR){
    if(data.busy=='true'){
      cleaningstatusalert(true, data.message)
      progressbar(data.busy)
    }
    else{
      cleaningstatusalert(false, data.message)
      progressbar(data.busy)
      clearInterval(checkStatusInterval)
    }
    
  }
  function checkCleaningError(jqXHR, textStatus, errorThrown){
    console.log(errorThrown)
    
  }
  return true
}
function cleaningstatusalert(show, message){
  alert = $('#id_cleaning_status')
  if(show==true){
    alert.removeClass('alert-success').addClass('alert-info')
    alert.html(message)
    alert.fadeIn()
  }
  else{
    alert.html(message)
    alert.removeClass('alert-info').addClass('alert-success')
    alert.fadeIn().delay(800).fadeOut( 400 );
  }
}

function progressbar(state){
  progress_obj = $('#id_clean_progress_bar')
  if(state=='true'){
    progress_obj.fadeIn()
    progressval = 50+'%'
    $('#id_clean_progress_bar').width(progressval)
    console.log(progressval);
  }
  else{
    progress_obj.fadeOut()
  }

}
$("#next_bttn_dina").on('click',function(e){
  $.when($("#dinamicpurgecard").fadeOut()).done(function() {
         $("#stepscounter").text('Step 3/3')
         $("#staticpurgecard").fadeIn();
         $("#restart_bttn_dina").show()
  });
})

$("#restart_bttn_dina").on('click',function(e){
  location.reload();
})
