app.controller("findNavController", function ($scope, $location, $state) {
    var findNavList = $scope.findNavList = [
        {
            'id': 'back_end',
            'title': '后端',
            'state': 'find.back_end({domain: "back_end"})',
        },
        {
            'id': 'fore_end',
            'title': '前端',
            'state': 'find.fore_end({domain: "fore_end"})',
        },
        {
            'id': 'IOS/Android',
            'title': '移动',
            'state': 'find.mobile({domain: "mobile"})',
        },
        {
            'id': 'operation',
            'title': '运维',
            'state': 'find.operation({domain: "operation"})',
        },
        {
            'id': 'product',
            'title': '产品',
            'state': 'find.product({domain: "product"})',
        },
        {
            'id': 'office_software',
            'title': '办公软件',
            'state': 'find.office_software({domain: "office_software"})',
        },
        {
            'id': 'design_software',
            'title': '设计软件',
            'state': 'find.design_software({domain: "design_software"})',
        },
    ]

    // var activeLinkView = "";
    // if ($location.url() == '/find') {
    //     activeLinkView = 'find.back_end';
    // }else {
    //     angular.forEach(findNavList, function (data) {
    //         if ($location.url() == '/' + data.linkView.substr(2)) {
    //             activeLinkView = data.linkView;
    //             return false;
    //         }
    //     });
    // }
    // if (activeLinkView != "") {
    //     $state.go(activeLinkView)
    // }
});