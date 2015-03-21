(function() {
    var app = angular.module('servicesApp', ['ngRoute']);

    app.config(['$routeProvider', '$locationProvider',

        function($routeProvider, $locationProvider) {
            $routeProvider

                .when('/services', {
                    templateUrl: '/static/angular/list.html',
                    controller: 'servicesController'
                })

                .when('/services/add', {
                    templateUrl: '/static/angular/add.html',
                    controller: 'addServiceController',
                })

                .otherwise({
                    templateUrl: '/static/angular/404.html'
                });

            $locationProvider.html5Mode({
              enabled: true,
              requireBase: false
            });

        }]);

    app.controller('servicesController', ['$http', '$scope', '$timeout', function($http, $scope, $timeout){
        $scope.services = [];
        $scope.is_loading = true;

        $scope.refresh = function(){
            $scope.is_loading = true;

            $http.get("/api/v1/service/?format=json")

                .success(function(data){
                    $scope.services = data.objects;
                    $scope.is_loading = false;

                })

                .error(function(data){
                    $scope.is_loading = false;
                    alert("Unable to refresh. Try again later.");
                });

        };

        $scope.refresh();
    }]);

    app.controller('addServiceController', ['$http', '$scope', function($http, $scope){

    }]);

})();