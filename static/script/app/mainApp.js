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
        templateUrl: 'view/find/content.html'
    })
    .state('/.domain', {
        url: ':domain',
        templateUrl: 'view/find/content.html'
    })
    .state('/./.language', {
        url: ':language',
        templateUrl: 'view/find/backEnd/content.html'
    })

    $urlRouterProvider.otherwise('/');
    $locationProvider.hashPrefix("");
});