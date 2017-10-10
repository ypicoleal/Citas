$(document).ready(function() {
    $("#id_fecha_").change(function(event) {
        /* Act on the event */
        if (this.value !== "") {
            calendarios($(this).val());

        }
    });

    console.log("ready", $("#id_confirmacion"));
    $("#id_confirmacion").change(function(event) {
        /* Act on the event */
        var motivo = $("#id_motivo");
        if (parseInt(this.value) == 2) {
            motivo.prop("disabled", false);
            motivo.prop('required', true);
            $('select').material_select();
        } else {
            motivo.prop("disabled", true);
            motivo.prop('required', false);
            $('select').material_select();
        }
    });
    cargando($("body"));
});

$(document).load(function() {
    console.log("ready", $("#id_confirmacion"));

});

function cargando(query) {
    var loading = `<div class="full-height"><div class="preloader-wrapper big active">
        <div class="spinner-layer spinner-purple-only">
            <div class="circle-clipper left">
                <div class="circle">
                </div>
            </div>
            <div class="gap-patch">
                <div class="circle">
                </div>
            </div>
            <div class="circle-clipper right">
                <div class="circle"></div>
                </div>
            </div>
        </div>
    </div>`;
    query.prepend(loading);
    $(".full-height").hide();
}

function calendarios(fecha) {
    var formatdate = fecha.split('/'),
        anio = parseInt(formatdate[2]),
        mes = parseInt(formatdate[1]),
        dia = parseInt(formatdate[0]);
    $(".full-height").show();

    $.ajax({
        url: '/agenda/calendario/list/',
        type: 'GET',
        dataType: 'json',
        data: {
            inicio__year: anio,
            inicio__month: mes,
            inicio__day: dia,
            almuerzo: 'False'
        },
        success: function(response, status, jqXHR) {
            var events = response.object_list,
                calendario = $("#id_calendario");
            calendario.html("");
            calendario.append('<option value="">---------</option>');
            events.forEach(function(element) {
                calendario.append('<option value="' + element.id + '">' + element.name + '</option>');
            });
            calendario.prop("disabled", false);
            $('select').material_select();
            $(".full-height").hide();
        },
        error: function(response, status, errorThrown) {
            if (response.status == 403) {
                alert(response.responseJSON.error);
            }
            $(".full-height").hide();
        }
    });
}
