app.controller("findNavController", function ($scope, $location, $state) {
    var findNavList = $scope.findNavList = [
        {
            'id': 'back_end',
            'title': '后端',
            'baseLink': '/.domain',
            'linkUrl': ''
        },
        {
            'id': 'fore_end',
            'title': '前端',
            'baseLink': '/.domain',
            'linkUrl': 'fore_end'
        },
        {
            'id': 'IOS/Android',
            'title': '移动',
            'baseLink': '/.domain',
            'linkUrl': 'mobile'
        },
        {
            'id': 'operation',
            'title': '运维',
            'baseLink': '/.domain',
            'linkUrl': 'operation'
        },
        {
            'id': 'product',
            'title': '产品',
            'baseLink': '/.domain',
            'linkUrl': 'product'
        },
        {
            'id': 'office_software',
            'title': '办公软件',
            'baseLink': '/.domain',
            'linkUrl': 'office_software'
        },
        {
            'id': 'design_software',
            'title': '设计软件',
            'baseLink': '/.domain',
            'linkUrl': 'design_software'
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