$(document).ready(function(){
    checkConnection();
})

let connectionCheckRoomName = 'oc_lab_status';
var connectionCheckSocket

connectionCheckSocket = new WebSocket('ws://' + window.location.host + '/ws/monitor/' + connectionCheckRoomName + '/');
connectionCheckSocket.onmessage = function(e) {
    checkConnection()
};

connectionCheckSocket.onclose = function(e) {
    console.error('Connection check can not be done');
};

function footerState(data){
    foot = $('#footer')
    footText = $('#footerText')
    if (data.connected==true){
      $('#footer').removeClass("bg-warning").addClass("bg-success");
      footText.html("2LabsToGo Connected to "+ data.port)
    } else{
      foot.removeClass("bg-success").addClass("bg-warning");
      footText.html("2LabsToGo Disconnected")
    }
}

function checkConnection(){
    $.get(window.location.origin + '/connection_info/').done(data=>footerState(data));
}





