var app = angular.module('myApp', ['ui.materialize', 'ngMessages', 'ngRoute']);

    app.config(function($interpolateProvider, $routeProvider ) {
    	$interpolateProvider.startSymbol('[[');
    	$interpolateProvider.endSymbol(']]');
      $routeProvider
      .when('/home', {
          templateUrl: '/encuestas/',
          controller: 'HomeController'
      })
      .when('/encuesta/:instrumento/:asignacion', {
          templateUrl: '/instrumento/',
          controller: 'EncuestaController'
      })
      .when('/perfil', {
          templateUrl: '/perfil/',
          controller: 'PerfilController'
      })
      .otherwise({
  			redirectTo: '/home'
  		});
    });

    app.controller('HomeController', function ($scope, $http, $window) {

        $scope.terminos = $window.sessionStorage.getItem('terminos');
        $scope.mensajeConfirmacion = 'En forma voluntaria expreso mi entendimiento sobre el objetivo del presente instrumento de recolección de información, la cual será usada con fines académicos e investigativos por medio del trabajo de grado “Herramienta informática para apoyar los medios de participación del egresado del Programa de Ingeniería de Sistemas de la Universidad de Cartagena”.';
        $scope.asignaciones = [];
        $scope.ready = true;

        $scope.confirmacion = function(){
          if (!$window.sessionStorage.getItem('terminos')) {
            $window.sessionStorage.setItem('terminos', '0');
              $scope.modal();
          }else if ($window.sessionStorage.getItem('terminos') == '0') {
              $scope.modal();
          }
        };
        $scope.closeModal = function (){
            $('.modal').modal('close');
        };

        $scope.modal = function (){
           $('.modal').modal({
                dismissible: true, // Modal can be dismissed by clicking outside of the modal
                opacity: .5, // Opacity of modal background
                inDuration: 300, // Transition in duration
                outDuration: 200, // Transition out duration
                startingTop: '4%', // Starting top style attribute
                endingTop: '10%', // Ending top style attribute
                ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
                },
                complete: function() {
                } // Callback for Modal close
              }
            );
            $('#modal2').modal('open');
        };
        $scope.confirmacion();

        $scope.acepto = function () {
          $window.sessionStorage.setItem('terminos', '1')
          $scope.terminos = '1';
        };

        $http({
          'url': '/banco/list/asignaciones/',
          'method': 'GET'
        }).then(function doneCallbacks(response){
          if (response.data.object_list.length) {
            $scope.asignaciones = response.data.object_list;
          }
          $scope.ready = false;
        }, function failCallbacks(response){
          console.log(response);
          $scope.ready = false;
        });
    });

    app.controller('EncuestaController', function($scope, $http, $routeParams, $location, $window){
      var instrumento = $routeParams.instrumento;
      $scope.instrumento = {};
      $scope.intrumentoParams = $routeParams.instrumento;
      $scope.asignacionParams = $routeParams.asignacion;
      $scope.respuestas = [];
      $scope.valid = [];
      $scope.ready = true;
      $scope.mensaje = "No se encontro ninguna encuesta";
      $scope.url = "#!/home";
      $scope.modal = function (){
         $('.modal').modal({
              dismissible: true, // Modal can be dismissed by clicking outside of the modal
              opacity: .5, // Opacity of modal background
              inDuration: 300, // Transition in duration
              outDuration: 200, // Transition out duration
              startingTop: '4%', // Starting top style attribute
              endingTop: '10%', // Ending top style attribute
              ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
                $scope.ready = false;
              },
              complete: function() {
                $location.path("#!/home");
              } // Callback for Modal close
            }
          );
          $('#modal1').modal('open');
      };

      $http({
        'url': '/encuesta/list/instrumentos/?id='+ instrumento,
        'method': 'GET'
      }).then(function doneCallbacks(response){
          if (response.data.object_list.length) {
            $scope.instrumento = response.data.object_list[0];
          }else {
            $scope.instrumento = false;
            $scope.modal();
          }
          $scope.ready = false;
      }, function failCallbacks(response){
          console.log(response);
          $scope.ready = false;
      });

      $scope.validacionForm = function(){
        var errors = 0;
        $scope.respuestas.forEach(function(element, index){
          if (Array.isArray(element.opciones)) {
            if (element.otro && element.otro !== "") {
              $scope.valid[index] = true;
            }else {
              if (element.opciones.length === 0) {
                  $scope.valid[index] = false;
                  errors ++;
              }else{
                  var validos = 0;
                  element.opciones.forEach(function(ele){
                    if (ele) {
                      validos++;
                    }
                  });
                  if (validos===0) {
                    $scope.valid[index] = false;
                    errors ++;
                  }else {
                    $scope.valid[index] = true;
                  }
              }
            }
          }else {
            if (element.otro && element.otro !== "") {
              $scope.valid[index] = true;
            }else {
              if (element.opciones === undefined) {
                $scope.valid[index] = false;
                errors ++;
              }else {
                $scope.valid[index] = true;
              }
            }
          }
        });
        if (errors===0) {
          return true;
        }else {
          return false;
        }
      };

      function formatData(data){
        var dataSend = {};
        dataSend.asignacion = $routeParams.asignacion;
        dataSend['cerrada_set-TOTAL_FORMS'] = $scope.instrumento.preguntasList.num_rows;
        dataSend['cerrada_set-INITIAL_FORMS'] = 0;
        dataSend['cerrada_set-MIN_NUM_FORMS'] = 0;
        dataSend['cerrada_set-MAX_NUM_FORMS'] = 1000;
        dataSend['otros_set-INITIAL_FORMS'] = 0;
        dataSend['otros_set-MIN_NUM_FORMS'] = 0;
        dataSend['otros_set-MAX_NUM_FORMS'] = 1000;
        var count = 0;
        data.forEach(function(element, index){
          if (element.opciones) {
            if (Array.isArray(element.opciones)) {
              element.opciones.forEach(function(obj){
                if (obj) {
                  dataSend['cerrada_set-'+ index +'-pregunta'] = element.pregunta;
                  dataSend['cerrada_set-'+ index +'-respuestas'] = [];
                  dataSend['cerrada_set-'+ index +'-respuestas'].push(obj.id);
                }
              });
            }else {
              if (element.opciones) {
                dataSend['cerrada_set-'+ index +'-pregunta'] = element.pregunta;
                dataSend['cerrada_set-'+ index +'-respuestas'] = [];
                dataSend['cerrada_set-'+ index +'-respuestas'].push(element.opciones.id);
              }
            }
          }
          if(element.otro){
            dataSend['otros_set-'+ count +'-pregunta'] = element.pregunta;
            dataSend['otros_set-'+ count +'-respuesta'] = element.otro;
            count ++;
          }
        });
        dataSend['otros_set-TOTAL_FORMS'] = count;
        return dataSend;
      }

      $scope.enviar = function (){
        $scope.mensaje = "Encuesta guardada con exito";
        $scope.ready = true;
        $http({
          'url': '/banco/formulario/',
          'method': 'POST',
          'data': formatData($scope.respuestas),
           headers: {
               'Content-Type': 'application/x-www-form-urlencoded'
           },
        }).then(function doneCallbacks(response){
          $scope.modal();
        },function failCallbacks(response){
          $scope.ready = false;
          if (response.status === 400) {
            if (response.data.__all__.length) {
              $scope.mensaje = response.data.__all__[0];
              $scope.modal();
            }
          }
        });
      };

    });

    app.controller('PerfilController' ,function($scope, $http){
        $scope.data = {};
        $scope.ready = true;
        $http({
          'url': '/usuarios/is/login/',
          'method': 'GET'
        }).then(function doneCallbacks(response){
            if (response.status == 200) {
              $scope.data = response.data;
            }
            $scope.ready = false;
        }, function failCallbacks(response){
            console.log(response);
            $scope.ready = false;
        });

        $scope.enviar = function(){

          $scope.ready = true;
          $http({
            'url': '/usuarios/diligenciador/edit/' + $scope.data.id + '/',
            'method': 'POST',
            'data': $scope.data,
             headers: {
                 'Content-Type': 'application/x-www-form-urlencoded'
             },
          }).then(function doneCallbacks(response){
              $scope.ready = false;
              Materialize.toast('Actualizado con exito!', 4000); // 4000 is the duration of the toast

          }, function failCallbacks(response){
            console.log(response);
          })
        };
    });
