(function() {
    var app = angular.module('servicesApp', ['ngRoute']);

    app.config(['$routeProvider',

        function($routeProvider) {
            $routeProvider
                .when('/', {
                    templateUrl: '/static/angular/list.html',
                    controller: 'ServicesController'
                })
                .when('/add', {
                    templateUrl: '/static/angular/add.html',
                    controller: 'AddServiceController'
                });
        }]);

    app.controller('ServicesController', ['$http', '$scope', '$timeout', function($http, $scope, $timeout){
        $scope.services = [];
        $scope.is_loading = true;
        $scope.seconds_left = 15;
        $scope.run_loop = true;

        $scope.refresh_loop = function() {
            $timeout(function(){
                $scope.seconds_left -= 1;
                if($scope.seconds_left <= 0){
                    $scope.seconds_left = 15;
                    $scope.refresh();
                }
                if($scope.run_loop)
                    $scope.refresh_loop();
            }, 999);
        };

        $scope.refresh = function(){
            $scope.is_loading = true;
            $http.get("/api/v1/service/?format=json").success(function(data){

                $scope.services = data.objects;
                $scope.is_loading = false;

            }).error(function(data){
                $scope.is_loading = false;
                alert("Unable to refresh. Try refershing the page manually.");
            });

        };


        $scope.refresh();
        // Refresh in 15 seconds
        $scope.refresh_loop();

        $scope.stop_loop = function () {
            // body...
            $scope.run_loop = false;
        }
    }]);

    app.controller('AddServiceController', ['$http', '$scope', '$timeout', function($http, $scope, $timeout){
        $scope.message = "ciupa";
    }]);

})();