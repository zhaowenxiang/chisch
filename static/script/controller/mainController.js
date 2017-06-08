app.controller('mainController', function ($rootScope, $scope, $location, $state) {
    console.log("index mainController");
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
    //console.log($state);
    //$state.transition('find');
    // console.log($location.url());
    // var activeLinkView = "";
    // if ($location.url() == '/' || $location.url() == '') {
    //     activeLinkView = 'find';
    // }else {
    //     angular.forEach(headerNavList, function (data) {
    //         if ($location.url() == '/' + data.state) {
    //             activeLinkView = data.state;
    //             return false;
    //         }
    //     });
    // }
    // if (activeLinkView != "") {
    //     $state.go(activeLinkView)
    // }
});