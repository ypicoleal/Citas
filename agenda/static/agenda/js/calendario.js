$(document).ready(function() {
    $(".right-panel").prepend('<div class="card"><div class="card-content"><a style="width: 100%;" href="#calendario" class="btn btn-primary import">Calendario</a></div></div>');
    addMOdal();
});


function addMOdal() {
    var cont = "<div id='calendario' class='modal'>" +
        "<div class='modal-content'>" +
        "<div id='calendar'>" +
        "</div>" +
        "</div>" +
        "</div>";
    $("body").append(cont);
    $('.modal').modal({
        ready: function(modal, trigger) {
            calendario();
        }
    });
}

function formModal(id) {
    var formTemplete = '<div class="modal" id="formModal">' +
        '<div class="modal-content">' +
        '<div class="row">' +
        '<form action="/agenda/calendario/form/' + id + '/" method="POST" class="col s12">' +
        '<div class="input-field col s12">' +
        '<input type="checkbox" name="almuerzo" value="" id="id_almuerzo">' +
        '<label for="id_almuerzo">Hora de almuerzo</label>' +
        '</div>' +
        '<div class="input-field col s6">' +
        '<a class="waves-effect waves-light btn"><i class="material-icons right">delete</i>Eliminar</a>' +
        '</div>' +
        '<div class="input-field col s6">' +
        '<button class="btn waves-effect waves-light" type="submit" name="action">Guardar' +
        '<i class="material-icons right">send</i>' +
        '</button>' +
        '</div>' +
        '</form>' +
        '</div>' +
        '</div>' +
        '</div>';

    if ($("#formModal").length === 0) {
        console.log("entrooo a if");
        $("body").append(formTemplete);
    }
    $("#formModal").modal();
    $('#formModal').modal('open');
}

function calendario() {
    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        locale: 'es',
        navLinks: true, // can click day/week names to navigate views
        selectable: true,
        selectHelper: true,
        defaultView: 'agendaWeek',
        select: function(start, end) {
            var fecha1 = new Date(start.format()),
                fecha2 = new Date(end.format()),
                resta = fecha2.getTime() - fecha1.getTime(),
                minutos = Math.round(resta / 60000);

            if (minutos == 30) {
                var eventData,
                    data;
                data = {
                    almuerzo: false,
                    inicio: start.format('Y-MM-DD hh:mm:ss'),
                    fin: end.format('Y-MM-DD hh:mm:ss')
                };
                Materialize.toast('Guardando', 2000);
                $.ajax({
                        url: '/agenda/calendario/form/',
                        type: 'POST',
                        dataType: 'json',
                        contentType: "application/json; charset=utf-8",
                        data: JSON.stringify(data)
                    })
                    .done(function(response) {
                        console.log(response);
                        eventData = {
                            id: response.id,
                            almuerzo: response.almuerzo,
                            title: 'Espacio para cita',
                            start: start,
                            end: end
                        };
                        $('#calendar').fullCalendar('renderEvent', eventData, true); // stick? = t
                    })
                    .fail(function(response) {
                        console.log(response);
                        console.log(response.responseJSON);
                        if (response.status == 400) {
                            if (response.responseJSON.fin) {
                                alert("Fecha final: " + response.responseJSON.fin[0]);
                            }
                            if (response.responseJSON.inicio) {
                                alert("Fecha inical: " + response.responseJSON.inicio[0])
                            }
                            if (response.responseJSON.__all__) {
                                alert(response.responseJSON.__all__[0])
                            }
                        }
                    });
            } else {
                Materialize.toast('Rango de fecha inválido, superior a 30 minutos.', 4000);
            }
            $('#calendar').fullCalendar('unselect');
        },
        editable: false,
        hiddenDays: [0],
        allDayDefault: false,
        allDaySlot: false,
        minTime: "08:00:00",
        maxTime: "19:00:00",
        slotLabelFormat: 'h(:mm)a',
        slotEventOverlap: false,
        eventLimit: true, // allow "more" link when too many events
        eventClick: function(calEvent, jsEvent, view) {
            console.log(calEvent);
            formModal(calEvent.id)
            // change the border color just for fun
            $(this).css('border-color', 'red');

        },
        events: function(start, end, timezone, callback) {
            var today = new Date();
            $.ajax({
                    url: '/agenda/calendario/list/',
                    type: 'GET',
                    dataType: 'json',
                    data: {
                        inicio__year: today.getFullYear(),
                        inicio__month: today.getMonth() + 1
                    }
                })
                .done(function(response) {
                    var events = response.object_list;
                    callback(events);
                })
                .fail(function(response) {
                    console.log("error");
                    console.log(response);
                })
                .always(function() {
                    console.log("complete");
                });
        }
    });

}
