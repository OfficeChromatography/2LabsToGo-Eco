async function sendToMachine(value) {
    const data = {'gcode': value};
    console.log(data);
    return new Promise(function(resolve, reject) {
        $.ajax({
            method: 'POST',
            url: window.location.origin + '/send/',
            data: data,
            success: function(data, textStatus, jqXHR) {
                console.log("Success!");
                resolve(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error("Error:", errorThrown);
                reject(errorThrown);
            }
        });
    });
}

async function openValve() {
    try {
        await sendToMachine('G0X1');                  // Waste bottle
        await sendToMachine('M400');
        await sendToMachine('M42P36S255');            // Activate 3-way valve
        await sendToMachine('G41');                   // Open dispensing valve
        await sendToMachine('G4S30');                 // Wait 30 seconds
        await sendToMachine('M42P36S0');              // Deactivate 3-way valve
    } catch (error) {
        console.error('Error in openValve:', error);
    }
}

$('#openvalve').on('click', function() {
    openValve();
});
