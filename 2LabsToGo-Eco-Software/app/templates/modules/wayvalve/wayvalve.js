$("#valvecontrol").on('click', function(e) {
    e.preventDefault();
    console.log($("#wayvalveControlForm").serialize());
    sendToValveControl();
});

function sendToValveControl() {
    $.ajax({
        method: 'POST',
        url: window.location.origin + '/wayvalve/',
        data: $("#wayvalveControlForm").serialize(),
        success: function(data, textStatus, jqXHR) {
            console.log("Success!");
            controlValve();
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log(errorThrown);
        }
    });
}

async function controlValve() {
    const cycles = parseInt($('#valveCycles').val(), 10);
    for (let i = 0; i < cycles; i++) {
        try {
            await sendToMachine('M42P36S255'); // Ventil aktivieren
            await sendToMachine('G4S1');     // 1 Sekunde warten
            await sendToMachine('M42P36S0');   // Ventil deaktivieren
            await sendToMachine('G4S1');     // 1 Sekunde warten
        } catch (error) {
            console.error('Error in controlValve:', error);
        }
    }
}

$('#valveRange').on('change', function() {
    $('#valveCycles').val($(this).val());
});

$('#valveCycles').on('change', function() {
    $('#valveRange').val($(this).val());
});

// Annahme: Diese Funktion wurde bereits in deinem Code definiert
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
