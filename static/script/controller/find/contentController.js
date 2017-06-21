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
    $scope.query = function (page_number) {
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
                    'page_size': 30,
                    'page_number': page_number,
                }
	        }
        }).then(function (response) {  //正确请求成功时处理
            angular.forEach(response.data.result.rows, function (record) {
                res.push(record);
            });
            $scope.total = response.data.result.pagination.total;
            $scope.page_num_array = []
            var page_count = Math.ceil($scope.total/30)
            for (var i=1; i<=page_count; i++) {
                $scope.page_num_array.push(i)
            }

            // console.log(result);
        }).catch(function (error) { //捕捉错误处理
            alert("failed");
            console.log(error);
        })
    }
    $scope.query();
    document.getElementById('price');

});