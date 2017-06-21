app.controller("findContentController", function ($scope, $location, $state, $stateParams, $http) {
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
        $location.search(queryCriteria);

        var res = $scope.res = new Array()

        $http({
	        method: 'POST',
	        url: 'http://120.77.213.246/api/curriculum',
            headers: {
	            'Content-Type': "application/json; charset=UTF-8",
            },
            data: {
	            action: 'page_list',
                params: {
                    'page_size': 1,
                    'page_number': 30,
                }
	        }
        }).then(function (response) {  //正确请求成功时处理
            console.log(response.data.result);
            angular.forEach(response.data.result, function (record) {
                res.push(record)
            });
            // console.log(result);
        }).catch(function (error) { //捕捉错误处理
            alert("failed");
            console.log(error);
        })
    }
    $scope.query();
    document.getElementById('price');

});