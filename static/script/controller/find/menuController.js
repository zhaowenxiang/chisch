app.controller("findBackEndController", function ($scope, $location, $state) {
    var backEndMenuList = $scope.backEndMenuList = [
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
});