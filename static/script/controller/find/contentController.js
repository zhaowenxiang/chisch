app.controller("findContentController", function ($scope, $location, $state, $stateParams) {
    $scope.language = $state.current.data.language;

    //url 中的查询条件
    console.log($location.search())
    var queryCriteria = $scope.queryCriteria = $location.search();

    // 默认选中排序规则（综合排序）
    if (queryCriteria.orderBy == undefined) {
        queryCriteria.orderRule = "comprehensive";
        //$scope.orderRule = "comprehensive";
    }else {

    }

    //过滤器
    queryCriteria.isFree = true;
    $scope.query = function () {
        // console.log($location.absUrl());
        console.log($location.search());
    }
});