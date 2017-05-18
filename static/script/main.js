requirejs.config({
    //baseUrl: "/root/git/chisch/static/lib/",
    paths: {
        'angular': "../lib/angularjs/angular",
    },
    shim: {
        "angular": {
            exports: "angular"
        }
    },
    urlArgs: "bust=" +  (new Date()).getTime()
});

requirejs([
    'angular',
    'service/userService',
], function () {
    console.log("load over");
});