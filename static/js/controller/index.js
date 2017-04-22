var app = angular.module('index_app', []);
app.controller('index_controller', function($scope) {

    $scope.user_name = "18701567211";
    $scope.password = "123456";

    $scope.login = function(){
        alert("zhaowenxaing");
	};
});