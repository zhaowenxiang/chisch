app.controller('mainController', function ($scope, $location, $state) {
    var headerNavList = $scope.headerNavList = [
        {
            'id': 'find',
            'title': '发现',
            'linkView': '/',
        },
        {
            'id': 'my',
            'title': '我的',
            'linkView': 'my',
        },
        {
            'id': 'friend',
            'title': '朋友',
            'linkView': 'friend',
        },
        {
            'id': 'market',
            'title': '商场',
            'linkView': 'market',
        },
        {
            'id': 'download',
            'title': 'APP下载',
            'linkView': 'download',
        }
    ]
});