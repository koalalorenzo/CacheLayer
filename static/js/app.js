(function() {
    var app = angular.module('servicesApp', ['ngRoute']);

    app.config(['$routeProvider', '$locationProvider',

        function($routeProvider, $locationProvider) {
            $routeProvider

                .when('/services', {
                    templateUrl: '/static/angular/list.html',
                    controller: 'servicesController'
                })

                .when('/services/new', {
                    templateUrl: '/static/angular/new.html',
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

    app.controller('servicesController', ['$http', '$scope', '$timeout', '$routeParams', function($http, $scope, $timeout, $routeParams){
        $scope.services = [];
        $scope.is_loading = true;

        $scope.refresh = function(){
            $scope.services = [];
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

        $scope.save = function(entry) {
            entry.store_days = parseInt(entry.store_days,10);
            entry.check_period = parseInt(entry.check_period,10);
            entry.request_timeout = parseInt(entry.request_timeout,10);
            entry.cache_duration = parseInt(entry.cache_duration,10);

            $http.post("/api/v1/service/", entry)
                .success(function(data){
                    console.log(data);
                    alert("Saved");
                    $scope.reset();
                })
                .error(function(data){
                    console.log(data);
                    alert("Unable to save");
                });
        };

        $scope.reset = function(form) {
            $scope.service = {};
        }

    }]);

})();