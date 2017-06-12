app.controller("findContentController", function ($scope, $location, $state, $stateParams) {
    $scope.language = $state.current.data.language;

    //初始化查询条件
    function initQueryCriteria(queryParams) {
        if (queryParams.orderBy == undefined) {
            queryParams.orderBy = "comprehensive";
        }else {

        }
        if (queryParams.isLookAt != undefined){
             (queryParams.isLookAt != 0)? queryParams.isLookAt = true: queryParams.isLookAt = false;
        }else {
            queryParams.isLookAt = false;
        }
        return queryParams
    }

    var queryCriteria = $scope.queryCriteria = initQueryCriteria($location.search());
    $location.search(queryCriteria);
    $scope.query = function () {
        console.log(queryCriteria);
        $location.search(queryCriteria);
    }
});