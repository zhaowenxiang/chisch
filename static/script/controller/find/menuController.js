app.controller("findMenuController", function ($scope, $location, $state, $stateParams) {
    var backEndMenuList = [
        {
            'id': 'python',
            'title': 'Python',
            'linkView': '/./.language',
        },
        {
            'id': 'java',
            'title': 'Java',
            'linkView': '/./.language',
        },
        {
            'id': 'ruby',
            'title': 'Ruby',
            'linkView': '/./.language',
        },
        {
            'id': 'golang',
            'title': 'Golang',
            'linkView': '/./.language',
        },
        {
            'id': 'c',
            'title': 'C',
            'linkView': '/./.language',
        },
        {
            'id': 'c++',
            'title': 'C++',
            'linkView': '/./.language',
        },
        {
            'id': 'basic',
            'title': 'Basic',
            'linkView': '/./.language',
        },
        {
            'id': 'pascal',
            'title': 'Pascal',
            'linkView': '/./.language',
        },
        {
            'id': 'erlang',
            'title': 'Erlang',
            'linkView': '/./.language',
        },
    ]
    var foreEndMenuList = [
        {
            'id': 'html',
            'title': 'Html',
            'linkView': '/./.language',
        },
        {
            'id': 'css',
            'title': 'CSS',
            'linkView': '/./.language',
        },
        {
            'id': 'javascript',
            'title': 'JavaScript',
            'linkView': '/./.language',
        }
    ]
    var mobileEndMenuList = [
        {
            'id': 'android',
            'title': 'Android',
            'linkView': '/./.language',
        },
        {
            'id': 'ios',
            'title': 'IOS',
            'linkView': '/./.language',
        }
    ]
    switch ($stateParams.domain) {
        case '':
            $scope.menuList = backEndMenuList;
            break;
        case 'fore_end':
            $scope.menuList = foreEndMenuList;
            break;
        case 'mobile':
            $scope.menuList = mobileEndMenuList;
            break;
    }
});