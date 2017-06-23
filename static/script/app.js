define(['angular'], function (angular) {
    var app = angular.module('mainApp', ['ui.router']);
    app.config(function ($stateProvider, $urlRouterProvider, $locationProvider) {
        $urlRouterProvider.when(
            '',
            'find/back_end/python'
        )
        $stateProvider
        //一级菜单
        .state('find', {
            url: '/find',
            templateUrl: 'view/find/nav.html',
            controller: 'findNavController',
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
        //发现下的二级菜单
        .state('find.back_end', {
            url: '/back_end',
            templateUrl: 'view/find/menu.html',
            data: {
                domain: "back_end"
            },
        })
        .state('find.fore_end', {
            url: '/fore_end',
            templateUrl: 'view/find/menu.html',
            data: {
                domain: "fore_end"
            }
        })
        .state('find.mobile', {
            url: '/mobile',
            templateUrl: 'view/find/menu.html',
            data: {
                domain: "mobile"
            }
        })
        .state('find.operation', {
            url: '/operation',
            templateUrl: 'view/find/menu.html',
            data: {
                domain: "operation"
            }
        })
        .state('find.product', {
            url: '/product',
            templateUrl: 'view/find/menu.html',
            data: {
                domain: "product"
            }
        })
        .state('find.office_software', {
            url: '/office_software',
            templateUrl: 'view/find/menu.html',
            data: {
                domain: "office_software"
            }
        })
        .state('find.design_software', {
            url: '/design_software',
            templateUrl: 'view/find/menu.html',
            data: {
                domain: "design_software"
            }
        })
        .state('find.back_end.python', {
            url: '/python',
            templateUrl: 'view/find/content.html',
            data: {
                language: "python",
                default_order: "Comprehensive",
            }
        })
        .state('find.back_end.java', {
            url: '/java',
            templateUrl: 'view/find/content.html',
            data: {
                language: "java"
            }
        })
        .state('find.back_end.ruby', {
            url: '/ruby',
            templateUrl: 'view/find/content.html',
            data: {
                language: "ruby"
            }
        })
        .state('find.back_end.golang', {
            url: '/golang',
            templateUrl: 'view/find/content.html',
            data: {
                language: "golang"
            }
        })
        .state('find.back_end.c', {
            url: '/c',
            templateUrl: 'view/find/content.html',
            data: {
                language: "c"
            }
        })
        .state('find.back_end.c++', {
            url: '/c++',
            templateUrl: 'view/find/content.html',
            data: {
                language: "c++"
            }
        })
        .state('find.back_end.basic', {
            url: '/basic',
            templateUrl: 'view/find/content.html',
            data: {
                language: "basic"
            }
        })
        .state('find.back_end.pascal', {
            url: '/pascal',
            templateUrl: 'view/find/content.html',
            data: {
                language: "pascal"
            }
        })
        .state('find.back_end.erlang', {
            url: '/erlang',
            templateUrl: 'view/find/content.html',
            data: {
                language: "erlang"
            }
        })
        .state('404', {
            url: '/404',
            templateUrl: '404.html',
        }),

        $urlRouterProvider.otherwise('/404');
        $locationProvider.hashPrefix("");
    });
    return app;
});