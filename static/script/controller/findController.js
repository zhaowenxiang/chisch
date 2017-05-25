app.controller("findController", function ($scope) {
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
});