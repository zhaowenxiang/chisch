var app = angular.module('mainApp', ['ui.router']);
app.config(function ($stateProvider, $urlRouterProvider, $locationProvider) {
    $stateProvider
    .state('/', {
        url: '/',
        templateUrl: 'view/find/nav.html'
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
        templateUrl: 'view/find/menu.html'
    })
    .state('/.domain', {
        url: ':domain',
        templateUrl: 'view/find/menu.html'
    })
    .state('/./.language', {
        url: ':language',
        templateUrl: 'view/find/content.html'
    })

    $urlRouterProvider.otherwise('/');
    $locationProvider.hashPrefix("");
});