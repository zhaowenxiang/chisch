define(['app'], function (app) {
    app.controller('mainController', function ($rootScope, $scope, $location, $state) {
        $scope.option_show = true;
        $scope.headerNavList = [
            {
                'title': '发现',
                'state': 'find'
            },
            {
                'title': '我的',
                'state': 'my'
            },
            {
                'title': '朋友',
                'state': 'friend'
            },
            {
                'title': '商场',
                'state': 'market'
            },
            {
                'title': 'APP下载',
                'state': 'download'
            }
        ];
    });
});
