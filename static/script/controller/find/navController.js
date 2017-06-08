app.controller("findNavController", function ($scope, $location, $state) {
    console.log("findNavController");
    var findNavList = $scope.findNavList = [
        {
            'id': 'back_end',
            'title': '后端',
            'state': 'find.back_end',
        },
        {
            'id': 'fore_end',
            'title': '前端',
            'state': 'find.fore_end',
        },
        {
            'id': 'IOS/Android',
            'title': '移动',
            'state': 'find.mobile',
        },
        {
            'id': 'operation',
            'title': '运维',
            'state': 'find.operation',
        },
        {
            'id': 'product',
            'title': '产品',
            'state': 'find.product',
        },
        {
            'id': 'office_software',
            'title': '办公软件',
            'state': 'find.office_software',
        },
        {
            'id': 'design_software',
            'title': '设计软件',
            'state': 'find.design_software',
        },
    ]
    if ($state.current.name == 'find') {
        $state.go('find.back_end');
    }
});