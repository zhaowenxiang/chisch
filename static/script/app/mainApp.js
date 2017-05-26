var app = angular.module('mainApp', ['ui.router']);
app.config(function ($stateProvider, $urlRouterProvider, $locationProvider) {
    $stateProvider
    .state('/', {
        url: '/',
        templateUrl: 'view/find/main.html'
    })
    .state('my', {
        url: '/my',
        templateUrl: 'view/my/main.html'
    })
    .state('friend', {
        url: '/friend',
        templateUrl: 'view/friend/main.html'
    })
    .state('market', {
        url: '/market',
        templateUrl: 'view/market/main.html'
    })
    .state('download', {
        url: '/download',
        templateUrl: 'view/download/main.html'
    })
    .state('/./', {
        url: '',
        templateUrl: 'view/find/backEnd.html'
    })
    .state('/.fore_end', {
        url: 'fore_end',
        templateUrl: 'view/find/foreEnd.html'
    })
    .state('/.mobile', {
        url: 'mobile',
        templateUrl: 'view/find/mobile.html'
    })
    .state('/.operation', {
        url: 'operation',
        templateUrl: 'view/find/operation.html'
    })
    .state('/.product', {
        url: 'product',
        templateUrl: 'view/find/product.html'
    })
    .state('/.office', {
        url: 'office',
        templateUrl: 'view/find/office.html'
    })
    .state('/.design', {
        url: 'design',
        templateUrl: 'view/find/design.html'
    })
    $urlRouterProvider.otherwise('/');
    $locationProvider.hashPrefix("");
});