app.controller("findController", function ($scope, $location, $state) {
    console.log($location.url());
    var findNavList = $scope.findNavList = [
        {
            'id': 'recommend',
            'title': '推荐',
            'linkView': '/./',
        },
        {
            'id': 'ranking',
            'title': '排行榜',
            'linkView': '/.ranking',
        },
        {
            'id': 'new',
            'title': '最新',
            'linkView': '/.new',
        },
        {
            'id': 'free',
            'title': '免费',
            'linkView': '/.free',
        },
    ]

    var activeLinkView = "";
    if ($location.url() == '/') {
        activeLinkView = '/./';
    }else {
        angular.forEach(findNavList, function (data) {
            if ($location.url() == '/' + data.linkView.substr(2)) {
                activeLinkView = data.linkView;
                return false;
            }
        });
    }
    if (activeLinkView != "") {
        $state.go(activeLinkView)
    }
});