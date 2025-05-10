var table_obj = null;

$(document).ready(function () {

    $('#waiting-time-modal-body').load(window.location.origin + '/development/waiting_time_view/', function () {
        table_obj = new TableWaitingTime();
        sincronizarModalConAplicaciones();
    });
    // Cuando el modal se abre, asegura que la tabla esté correctamente generada
    $('#modalwaitingtimes').on('shown.bs.modal', function () {
        if (table_obj) {
            table_obj.generateEmptyRows();
        }
    });

    // Cuando el modal se oculta, actualiza los datos
    $('#modalwaitingtimes').on('hide.bs.modal', function () {
        if (table_obj) {
            table_obj.updateWaitingTimesData();
        }
    });

    // Sincronizar la tabla cuando el número de aplicaciones cambie
    $("input[name='applications']").on("change", function () {
        sincronizarModalConAplicaciones();
    });
});

// $('#modalwaitingtimes').on('shown.bs.modal', function () {
//     if (table_obj) {
//         table_obj.generateEmptyRows();
//     }
// });

// $('#modalwaitingtimes').on('hide.bs.modal', function () {
//     if (table_obj) {
//         table_obj.updateWaitingTimesData();
//     }
// });

// $("input[name='applications']").on("change", function () {
//     sincronizarModalConAplicaciones();
// });

function sincronizarModalConAplicaciones() {
    const numApplications = parseInt($("input[name='applications']").val()) || 3;

    if (table_obj) {
        table_obj.generateEmptyRows();  
    }
}
