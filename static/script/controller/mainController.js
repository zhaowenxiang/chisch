define(['app'], function (app) {
    app.controller('mainController', function ($rootScope, $scope, $location, $state) {
    var headerNavList = $scope.headerNavList = [
        {
            'id': 'find',
            'title': '发现',
            'state': 'find'
        },
        {
            'id': 'my',
            'title': '我的',
            'state': 'my'
        },
        {
            'id': 'friend',
            'title': '朋友',
            'state': 'friend'
        },
        {
            'id': 'market',
            'title': '商场',
            'state': 'market'
        },
        {
            'id': 'download',
            'title': 'APP下载',
            'state': 'download'
        }
    ];
});
});
