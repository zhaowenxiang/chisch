var app = angular.module('mainApp', ['ui.router']);
app.config(function ($stateProvider, $urlRouterProvider, $locationProvider) {
    $stateProvider
    //一级菜单
    .state('/', {
        url: '/find',
        templateUrl: 'view/find/nav.html'
    })
    .state('find', {
        url: '/find',
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
    //二级发现菜单
    .state('find.back_end', {
        url: '/:domain',
        templateUrl: 'view/find/menu.html'
    })
    .state('find.fore_end', {
        url: '/:domain',
        templateUrl: 'view/find/menu.html',
    })
    .state('find.mobile', {
        url: '/:domain',
        templateUrl: 'view/find/menu.html',
    })
    .state('find.operation', {
        url: '/:domain',
        templateUrl: 'view/find/menu.html',
    })
    .state('find.product', {
        url: '/:domain',
        templateUrl: 'view/find/menu.html',
    })
    .state('find.office_software', {
        url: '/:domain',
        templateUrl: 'view/find/menu.html',
    })
    .state('find.design_software', {
        url: '/:domain',
        templateUrl: 'view/find/menu.html',
    })
    .state('find.back_end.python', {
        url: '/python',
        templateUrl: 'view/find/content.html'
    })
    //三级语言选择
    .state('/./.language', {
        url: ':language',
        templateUrl: 'view/find/content.html'
    })

    $urlRouterProvider.otherwise('/');
    $locationProvider.hashPrefix("");
});