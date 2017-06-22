requirejs.config({
    paths: {
        "jquery" : "../lib/jquery/jquery-3.2.1.min",
        "angular" : "../lib/angularjs/angular.min",
        'ngRoute': "../lib/angularjs/angular-route.min",
        "uiRoute" : "../lib/angularjs/angular-ui-route.min",
    },
    shim: {
        "angular" : {
            deps : ["jquery"],
            exports : "angular"
        },
        "jquery" : {
            exports : "jquery"
        },
        "uiRoute" : {
            deps : ["angular"]
        },
    }
});


requirejs([
    'angular',
    'uiRoute',
    'app/mainApp',
    'controller/mainController',
    'controller/find/navController',
    'controller/find/menuController',
    'controller/find/contentController'
], function () {
    console.log("load over");
});