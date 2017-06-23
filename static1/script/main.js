/**
* Created by Charles on 2014/11/14.
*/

require.config({
    paths: {
        "jquery" : "../lib/jquery/jquery-3.2.1.min",
        "angular" : "../lib/angularjs/angular.min",
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


require([
    "angular",
    "jquery",
    "uiRoute",
    "app",
    'controller/mainController',
    'controller/find/navController',
    'controller/find/menuController',
    'controller/find/contentController'
], function (angular, app) {
    angular.bootstrap(document,['mainApp']);
});
