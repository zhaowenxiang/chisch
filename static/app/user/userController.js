define(function () {
    app = angular.module('main', [])
    app.constructor('userController', ['userService'], function (userService) {
        console.log(userService.user.name)
    });
});