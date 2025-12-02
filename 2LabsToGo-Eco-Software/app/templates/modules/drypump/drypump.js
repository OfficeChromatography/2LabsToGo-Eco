async function sendToMachine(value) {
    var data = {'gcode': value};
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
                console.log(errorThrown);
                reject(errorThrown);
            }
        });
    });
}

async function controlPump(cycles) {
    for (let i = 0; i < cycles; i++) {
        try {
            await sendToMachine('M42 P40 S255'); // Pumpe ansaugen
            await sendToMachine('M400');
            await sendToMachine('M42 P40 S0');   // Pumpe pumpen
            await sendToMachine('M400');
            await new Promise(resolve => setTimeout(resolve, 1000)); // 1 Sekunde warten (falls nötig)
        } catch (error) {
            console.error('Error in controlPump:', error);
        }
    }
}

// Event-Listener für das Formular
document.getElementById('pumpControlForm').addEventListener('submit', function(event){
    event.preventDefault();
    var cycles = document.getElementById('pumpCycles').value;  // Wert aus dem Nummernfeld holen
    controlPump(parseInt(cycles, 10)); // Parse cycles to integer
});

// Synchronisation zwischen Range-Input und Number-Input
document.getElementById('pumpRange').addEventListener('input', function() {
    document.getElementById('pumpCycles').value = this.value;
});

document.getElementById('pumpCycles').addEventListener('input', function() {
    document.getElementById('pumpRange').value = this.value;
});
