$(document).ready(function() {
    $("#id_fecha_").change(function(event) {
        /* Act on the event */
        if (this.value !== "") {
            calendarios($(this).val());

        }
    });
    $("#id_confirmacion").change(function(event) {
        /* Act on the event */
        console.log(parseInt(this.value));
        if (parseInt(this.value) !== 2) {
            $("#id_motivo").prop("disabled", false);
            $("#id_motivo").prop('required', true);
            console.log("entro al if");
        } else {
            $("#id_motivo").prop("disabled", true);
            $("#id_motivo").prop('required', false);
            console.log("entro al esle");
        }
    });
    cargando($("body"));
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
    console.log(anio, mes);
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
