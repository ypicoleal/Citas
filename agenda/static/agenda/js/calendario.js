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



function formModal(id, self) {
    var url = "/agenda/calendario/form/' + id + '/";

    var formTemplete = `<div class="modal modal-c" id="formModal">
    <div class="modal-content">
    <div class="row row-no-mb">
        <div class="col s6">
            <a href="#" class="row row-no-mb tooltipped" data-tooltip="Asignar Almuerzo">
                <div class="col s12">
                    <div class="card">
                        <div class="card-image">
                            <img src="/static/img/almuerzo.svg">
                        </div>
                    </div>
                </div>
            </a>
        </div>
        <div class="col s6">
            <a href="#" class="row row-no-mb tooltipped" data-tooltip="Asignar cita">
                <div class="col s12">
                    <div class="card">
                        <div class="card-image">
                            <img src="/static/img/cita.svg" alt="">
                        </div>
                    </div>
                </div>
            </a>
        </div>
    </div>
    </div>
    </div>`;

    if ($("#formModal").length === 0) {
        console.log("entrooo a if");
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
                $(".full-height").show();
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
                            color: '#2196f3',
                            start: start,
                            end: end
                        };
                        $('#calendar').fullCalendar('renderEvent', eventData, true);
                        Materialize.toast('Guardado exitoso.', 2000);

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
                    }).always(function() {
                        $(".full-height").hide();
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
            formModal(calEvent.id, this);
            // change the border color just for fun
            //$(this).css('border-color', 'red');

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
                    $(".full-height").hide();
                });
        }
    });

}
