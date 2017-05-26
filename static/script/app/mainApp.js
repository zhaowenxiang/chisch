var app = angular.module('mainApp', ['ui.router']);
app.config(function ($stateProvider, $urlRouterProvider, $locationProvider) {
    $stateProvider
    .state('/', {
        url: '',
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
        templateUrl: 'view/find/recommend.html'
    })
    .state('/.ranking', {
        url: '',
        templateUrl: 'view/find/ranking.html'
    })
    .state('/.new', {
        url: '',
        templateUrl: 'view/find/new.html'
    })
    .state('/.free', {
        url: '',
        templateUrl: 'view/find/free.html'
    })
    $urlRouterProvider.otherwise('/');
    $locationProvider.hashPrefix("");
});