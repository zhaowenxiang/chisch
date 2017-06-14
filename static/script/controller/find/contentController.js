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
        console.log(queryCriteria);
        $location.search(queryCriteria);

        var res = $scope.res = [
            {
                "id": 1,
                "title": queryCriteria.orderBy,
            },
            {
                "id": 2,
                "title": queryCriteria.orderBy,
            },
            {
                "id": 3,
                "title": queryCriteria.orderBy,
            },
            {
                "id": 4,
                "title": queryCriteria.orderBy,
            },
            {
                "id": 5,
                "title": queryCriteria.orderBy,
            },
            {
                "id": 6,
                "title": queryCriteria.orderBy,
            },
            {
                "id": 7,
                "title": queryCriteria.orderBy,
            },
            {
                "id": 8,
                "title": queryCriteria.orderBy,
            },
            {
                "id": 9,
                "title": queryCriteria.orderBy,
            },
            {
                "id": 10,
                "title": queryCriteria.orderBy,
            },
            {
                "id": 11,
                "title": queryCriteria.orderBy,
            },
            {
                "id": 12,
                "title": queryCriteria.orderBy,
            },
            {
                "id": 13,
                "title": queryCriteria.orderBy,
            }
        ]
        $http({
	        method: 'POST',
	        url: 'http://120.77.213.246/api/curriculum',
            headers: {
	            'Content-Type': "application/json; charset=UTF-8",
            },
            data: {
	            action: 'page_list',
                params: {

                }
	        }
        }).then(function (result) {  //正确请求成功时处理
            console.log(result);
            alert("success");
            // console.log(result);
        }).catch(function (result) { //捕捉错误处理
            alert("failed");
            console.log(result);
        })
    }
});