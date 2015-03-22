(function() {
    var app = angular.module('servicesApp', ['ngRoute']);

    app.config(['$routeProvider', '$locationProvider',

        function($routeProvider, $locationProvider) {
            $routeProvider

                .when('/services', {
                    templateUrl: '/static/angular/list.html',
                    controller: 'servicesController'
                })

                .when('/service/:id/', {
                    templateUrl: '/static/angular/service.html',
                    controller: 'serviceController',
                })

                .when('/service/:id/edit/', {
                    templateUrl: '/static/angular/edit.html',
                    controller: 'editServiceController',
                })

                .when('/services/new', {
                    templateUrl: '/static/angular/edit.html',
                    controller: 'editServiceController',
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
                    $location.path('404');
                });
        };

        $scope.refresh();
    }]);

    app.controller('editServiceController', ['$http', '$scope', '$location', '$routeParams', function($http, $scope, $location, $routeParams){
        $scope.service = {};
        $scope.is_loading = true;

        if($location.path() === "/services/new")
        {
            $scope.service_url = "/api/v1/service/";
        }else{
            $scope.service.id = $routeParams.id;
            $scope.service_url = "/api/v1/service/"+$routeParams.id+"/";

            $http.get("/api/v1/service/"+$scope.service.id+"/?format=json")

                .success(function(data){

                    $scope.service = data;
                    $scope.is_loading = false;
                })

                .error(function(data){
                    $scope.is_loading = false;
                    alert("Unable to refresh. Try again later.");
                });

        }

        $scope.save = function(entry) {
            entry.store_days = parseInt(entry.store_days,10);
            entry.check_period = parseInt(entry.check_period,10);
            entry.request_timeout = parseInt(entry.request_timeout,10);
            entry.cache_duration = parseInt(entry.cache_duration,10);

            $http.post($scope.service_url, entry)
                .success(function(data){
                    console.log(data);
                    alert("Saved");
                    $scope.reset();
                    $location.path('service/'+data.id);
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

    app.controller('serviceController', ['$http', '$scope', '$routeParams', function($http, $scope, $routeParams){
        $scope.service = {};
        $scope.is_loading = true;

        $scope.get_service = function(service_id){
            $scope.service = {};
            $scope.is_loading = true;

            $http.get("/api/v1/service/"+service_id+"/?format=json")

                .success(function(data){

                    $scope.service = data;
                    $scope.is_loading = false;
                })

                .error(function(data){
                    $scope.is_loading = false;
                    alert("Unable to refresh. Try again later.");
                });
        };

        $scope.get_service($routeParams.id);

    }]);
})();