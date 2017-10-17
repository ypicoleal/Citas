$(document).ready(function() {
    //$(".right-panel").prepend('<div class="card"><div class="card-content"><a style="width: 100%;" href="#calendario" class="btn btn-primary import">Calendario</a></div></div>');
    //addMOdal();
    $(".right-panel").remove();
    var cont = $(".left-panel div div div div div");
    cont.html("<div id='calendar'></div>");
    cargando(cont);
    calendario();
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
}

function des(estado) {
    if (estado) {
        return "Desasignar"
    }
    return "Asignar"
}

function hideCita(estado) {
    if (estado) {
        return "none";
    }
    return "inherit";
}

function formModal(data, self) {
    if (data.asignacionCita == null) {
        var formTemplete = `<div class="modal modal-c" id="formModal">
        <div class="modal-content">
        <div class="collection">
            <a href="#!" class="collection-item"  onclick="asignarAlmuerzo(${data.id}, ${data.almuerzo})"><i class="material-icons">local_dining</i>${des(data.almuerzo)} almuerzo</a>
            <!--a href="#!" style="display: ${hideCita(data.almuerzo)};" class="collection-item"><i class="material-icons">event</i> Asignar cita</a-->
            <a href="#!" class="collection-item" onclick="eliminarCalendario(${data.id})"><i class="material-icons">delete</i>Eliminar</a>
        </div>
        </div>
        </div>`;

        var query = $("#formModal");
        if (query.length === 0) {
            $("body").append(formTemplete);
        } else {
            query.remove();
            $("body").append(formTemplete);
        }
        $("#formModal").modal({
            ready: function(modal, trigger) {
                $('.tooltipped').tooltip({
                    delay: 50,
                    position: 'right'
                });
            }
        });
        $('#formModal').modal('open');
    }
}

function eliminarCalendario(id) {
    $('#formModal').modal('close');
    if (confirm("¿Está seguro que desea borrar este calendario?") == true) {
        $.ajax({
            url: '/agenda/calendario/form/' + id + '/',
            type: 'POST',
            dataType: 'json',
            data: {
                eliminado: true
            },
            success: function(response) {
                $("#calendar").fullCalendar('removeEvents');
                $("#calendar").fullCalendar('refetchEvents');
                Materialize.toast('Borrado exitoso.', 2000);
            },
            error: function(response) {
                if (response.status == 400) {
                    alert(response.responseJSON.error);
                }
            }
        });
    }
}

function asignarAlmuerzo(id, estado) {
    $('#formModal').modal('close');
    $.ajax({
        url: '/agenda/calendario/form/' + id + '/',
        type: 'POST',
        dataType: 'json',
        data: {
            almuerzo: !estado
        },
        success: function(response) {
            $("#calendar").fullCalendar('refetchEvents');
            Materialize.toast('Guardado exitoso.', 2000);
        },
        error: function(response) {
            if (response.status == 400) {
                alert(response.responseJSON.error);
            }
        }
    });
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
                    inicio: start.format('Y-MM-DD HH:mm:ss'),
                    fin: end.format('Y-MM-DD HH:mm:ss')
                };
                $(".full-height").show();
                $.ajax({
                    url: '/agenda/calendario/form/',
                    type: 'POST',
                    dataType: 'json',
                    contentType: "application/json; charset=utf-8",
                    data: JSON.stringify(data),
                    success: function(response) {
                        eventData = {
                            id: response.id,
                            almuerzo: response.almuerzo,
                            title: 'Espacio para cita',
                            color: '#2196f3',
                            start: start,
                            end: end
                        };
                        $('#calendar').fullCalendar('renderEvent', eventData, true);
                        Materialize.toast('Guardado exitoso.', 1000);
                        $(".full-height").hide();

                    },
                    error: function(response) {
                        if (response.status == 400) {
                            if (response.responseJSON.fin) {
                                alert("Fecha final: " + response.responseJSON.fin[0]);
                            }
                            if (response.responseJSON.inicio) {
                                alert("Fecha inical: " + response.responseJSON.inicio[0]);
                            }
                            if (response.responseJSON.__all__) {
                                alert(response.responseJSON.__all__[0]);
                            }
                        } else if (response.status == 403) {
                            alert(response.responseJSON.error);
                        }
                        $(".full-height").hide();

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
            formModal(calEvent, this);
            // change the border color just for fun
            //$(this).css('border-color', 'red');

        },
        events: function(start, end, timezone, callback) {
            $(".full-height").show();
            var date = new Date($('#calendar').fullCalendar('getDate').format());
            $.ajax({
                url: '/agenda/calendario/list/',
                type: 'GET',
                dataType: 'json',
                data: {
                    inicio__year: date.getFullYear(),
                    inicio__month: date.getMonth() + 1
                },
                success: function(response, status, jqXHR) {
                    var events = response.object_list;
                    callback(events);
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
    });
    $('.fc-prev-button').click(function() {
        $("#calendar").fullCalendar('refetchEvents');
    });

    $('.fc-next-button').click(function() {
        $("#calendar").fullCalendar('refetchEvents');
    });
}
