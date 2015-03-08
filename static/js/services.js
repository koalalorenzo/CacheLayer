(function() {
    var app = angular.module('services', []);

    app.controller('ServicesController', ['$http', '$scope', function($http, $scope){
        $scope.services = [];
        $scope.is_loading = true;

        $scope.refresh = function(){
            $scope.is_loading = true;
            $http.get("/api/v1/service/?format=json").success(function(data){

                $scope.services = data.objects;
                $scope.is_loading = false;

                // Refresh in 5 seconds
                setTimeout(function(){
                    $scope.refresh();
                }, 5000);

            }).error(function(data){
                $scope.is_loading = false;
                alert("Unable to refresh. Try refershing the page manually.");
            });

        };

        $scope.refresh();
    }]);

})();