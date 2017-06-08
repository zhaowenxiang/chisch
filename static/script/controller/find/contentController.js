app.controller("findContentController", function ($scope, $location, $state, $stateParams) {
    $scope.language = $state.current.data.language;
});