function sendToMachine(value) {
    var data = {'gcode': value};
    console.log(data);
    $.ajax({
        method: 'POST',
        url: window.location.origin + '/send/',
        data: data,
        success: setHommingEndpointSuccess,
        error: setHommingEndpointError,
    });
}

function setHommingEndpointSuccess(data, textStatus, jqXHR) {
    console.log("Success!");
}

function setHommingEndpointError(jqXHR, textStatus, errorThrown) {
    console.log(errorThrown);
}

// Function to control the pump for specified number of strokes
async function controlPump(cycles) {
    for (let i = 0; i < cycles; i++) {
        sendToMachine('G50');
        sendToMachine('G4P250');
        sendToMachine('G51');
        sendToMachine('G4P250');
    }
}

// Event-Listener for the form
document.getElementById('pumpControlForm').addEventListener('submit', function(event){
    event.preventDefault();
    var cycles = document.getElementById('pumpCycles').value;
    controlPump(cycles);
});

// Synchronization Range-Input and Number-Input
document.getElementById('pumpRange').addEventListener('input', function() {
    document.getElementById('pumpCycles').value = this.value;
});

document.getElementById('pumpCycles').addEventListener('input', function() {
    document.getElementById('pumpRange').value = this.value;
});

function setHommingEndpointSuccess(response) {
    console.log('Success:', response);
}

function setHommingEndpointError(error) {
    console.error('Error:', error);
}
