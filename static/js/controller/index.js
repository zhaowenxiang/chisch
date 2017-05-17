var app = angular.module('index', []);

app.value('defaultInput', 5000);
app.factory('MathService', function () {
    var factory = {};
    factory.multiply = function (a, b) {
        return a * b;
    };
    return factory;
});

app.controller('indexController', function ($scope,  $location, $http, $timeout, $interval, CalcService, defaultInput) {
    $scope.names = [
        {name:'Jani',country:'Norway'},
        {name:'Hege',country:'Sweden'},
        {name:'Kai',country:'Denmark'},
        {name:'Kai1',country:'zzzz'},
        {name:'11',country:'Kai'}
    ];
    $scope.money = 100;
    $scope.url = $location.absUrl();
    $timeout(function () {
        $scope.myHeader = "How are you today?";
    }, 3000);
    $interval(function () {
        $scope.theTime = new Date().toLocaleTimeString();
    }, 1000);

    $scope.master = {firstName: "John", lastName: "Doe"};

    $scope.reset = function () {
        $scope.user = angular.copy($scope.master);
    };
    $scope.reset();
    console.log(CalcService.square())
});


//自定义过滤器
app.filter('reverse', function () {
   return function (text) {
        return text.split("").reverse().join("");
   };
});

//自定义服务
app.service('CalcService', function (MathService) {
    this.square = function (a) {
        return MathService.multiply(a,a)
    };
});

app.directive('runoobDirective', function () {
   return {
       template: "<h1>我在指令中被创建</h1>"
   }
});

