app.controller("findController", function ($scope, $location, $state) {
    var findNavList = $scope.findNavList = [
        {
            'id': 'back_end',
            'title': '后端',
            'linkView': '/./',
        },
        {
            'id': 'fore_end',
            'title': '前端',
            'linkView': '/.fore_end',
        },
        {
            'id': 'IOS/Android',
            'title': '移动',
            'linkView': '/.mobile',
        },
        {
            'id': 'operation',
            'title': '运维',
            'linkView': '/.operation',
        },
        {
            'id': 'product',
            'title': '产品',
            'linkView': '/.product',
        },
        {
            'id': 'office_software',
            'title': '办公软件',
            'linkView': '/.office',
        },
        {
            'id': 'design_software',
            'title': '设计软件',
            'linkView': '/.design',
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