app.controller("findMenuController", function ($scope, $location, $state, $stateParams) {
    var backEndMenuList = [
        {
            'id': 'python',
            'title': 'Python',
            'state': 'find.back_end.python({language: "python"})',
        },
        {
            'id': 'java',
            'title': 'Java',
            'state': 'find.back_end.java({language: "java"})',
        },
        {
            'id': 'ruby',
            'title': 'Ruby',
            'state': 'find.back_end.ruby({language: "ruby"})',
        },
        {
            'id': 'golang',
            'title': 'Golang',
            'state': 'find.back_end.golang({language: "golang"})',
        },
        {
            'id': 'c',
            'title': 'C',
            'state': 'find.back_end.c({language: "c"})',
        },
        {
            'id': 'c++',
            'title': 'C++',
            'state': 'find.back_end.c++({language: "c++"})',
        },
        {
            'id': 'basic',
            'title': 'Basic',
            'state': 'find.back_end.basic({language: "basic"})',
        },
        {
            'id': 'pascal',
            'title': 'Pascal',
            'state': 'find.back_end.pascal({language: "pascal"})',
        },
        {
            'id': 'erlang',
            'title': 'Erlang',
            'state': 'find.back_end.erlang({language: "erlang"})',
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
    switch ($stateParams.domain) {
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
});