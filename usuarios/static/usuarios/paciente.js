$(document).ready(function() {
    $("#id_fecha_nacimiento").change(function(event) {
        /* Act on the event */
        var fecha = this.value,
            formatdate = fecha.split('/'),
            nuevaFecha = formatdate[1] + '/' + formatdate[0] + '/' + formatdate[2],
            edad = calcularEdad(nuevaFecha),
            nombre_a = $("#id_nombre_a"),
            cedulad_a = $("#id_cedula_a");
        if (edad < 18) {
            nombre_a.prop('disabled', false);
            cedulad_a.prop('disabled', false);
        } else {
            nombre_a.prop('disabled', true);
            cedulad_a.prop('disabled', true);
            nombre_a.val('');
            cedulad_a.val('');
        }
    });


});

function calcularEdad(fecha) {
    var hoy = new Date();
    var cumpleanos = new Date(fecha);
    var edad = hoy.getFullYear() - cumpleanos.getFullYear();
    var m = hoy.getMonth() - cumpleanos.getMonth();
    if (m < 0 || (m === 0 && hoy.getDate() < cumpleanos.getDate())) {
        edad--;
    }
    return edad;
}
