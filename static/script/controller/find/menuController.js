app.controller("findMenuController", function ($scope, $location, $state, $stateParams) {
    console.log('findMenuController');
    var backEndMenuList = [
        {
            'id': 'python',
            'title': 'Python',
            'state': 'find.back_end.python',
        },
        {
            'id': 'java',
            'title': 'Java',
            'state': 'find.back_end.java',
        },
        {
            'id': 'ruby',
            'title': 'Ruby',
            'state': 'find.back_end.ruby',
        },
        {
            'id': 'golang',
            'title': 'Golang',
            'state': 'find.back_end.golang',
        },
        {
            'id': 'c',
            'title': 'C',
            'state': 'find.back_end.c',
        },
        {
            'id': 'c++',
            'title': 'C++',
            'state': 'find.back_end.c++',
        },
        {
            'id': 'basic',
            'title': 'Basic',
            'state': 'find.back_end.basic',
        },
        {
            'id': 'pascal',
            'title': 'Pascal',
            'state': 'find.back_end.pascal',
        },
        {
            'id': 'erlang',
            'title': 'Erlang',
            'state': 'find.back_end.erlang',
        },
    ]
    var foreEndMenuList = [
        {
            'id': 'html',
            'title': 'Html',
            'state': '/./.language',
        },
        {
            'id': 'css',
            'title': 'CSS',
            'state': '/./.language',
        },
        {
            'id': 'javascript',
            'title': 'JavaScript',
            'state': '/./.language',
        }
    ]
    var mobileEndMenuList = [
        {
            'id': 'android',
            'title': 'Android',
            'state': '/./.language',
        },
        {
            'id': 'ios',
            'title': 'IOS',
            'state': '/./.language',
        }
    ]   
    switch ($state.current.data.domain) {
        case '':
            $scope.menuList = backEndMenuList;
            break;
        case 'back_end':
            $scope.menuList = backEndMenuList;
            break;
        case 'fore_end':
            $scope.menuList = foreEndMenuList;
            break;
        case 'mobile':
            $scope.menuList = mobileEndMenuList;
            break;
    }
    if ($state.current.name == 'find.back_end') {
        $state.go('find.back_end.python');
    }

});