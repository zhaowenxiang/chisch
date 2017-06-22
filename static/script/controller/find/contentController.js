app.controller("findContentController", function ($scope, $location, $state, $stateParams, $http) {
    $scope.language = $state.current.data.language;
    $scope.inputPageNum = 1;

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
        if (queryParams.page == undefined) {
            queryParams.page = 1;
        }
        return queryParams
    }
    var queryCriteria = $scope.queryCriteria = initQueryCriteria($location.search());

    var results = $scope.results = {
        'pagination': {},
        'rows': [],
        'pageCount': null,
        'pageBtnArray':[],
        'pageNum': null,
    };

    $scope.query = function (pageNum, page_size) {
        reset_results(results);
        pageNum = new Number(pageNum);
        if (pageNum <= 0) {
            pageNum = 1;
        }
        queryCriteria.page = pageNum;
        $location.search(queryCriteria);
        $http({
	        method: 'POST',
	        url: 'http://localhost:8000/api/curriculum',
            headers: {
	            'Content-Type': "application/json; charset=UTF-8",
            },
            data: {
	            action: 'page_list',
                params: {
                    'page_size': 30,
                    'page_num': pageNum,
                }
	        }
        }).then(function (response) {  //正确请求成功时处理
            console.log(response.data, pageNum);
            wrapResult(response.data.result, pageNum);
        }).catch(function (error) { //捕捉错误处理
            alert("failed");
            console.log(error);
        })
    };
    
    var wrapResult = function (result, pageNum) {
        results.pagination = result.pagination;
        results.rows = result.rows;
        results.pageCount = Math.ceil(result.pagination.total/30);
        results.currentPage = pageNum;
        result.pageBtnArray = [];

        var pageBtnShowCount = 5;
        var pageBtnIndexList = [pageNum];

        for (var i=1; i<=results.pageCount-1; i++) {
            if (pageBtnIndexList.length == pageBtnShowCount) {
                break;
            }
            if (pageNum-i > 0) {
                pageBtnIndexList.push(pageNum - i)
            }
            if (pageNum+i <= results.pageCount) {
                pageBtnIndexList.push((pageNum + i))
            }
        }
        angular.forEach(pageBtnIndexList.sort(), function (page) {
            results.pageBtnArray.push({
                'page': page,
                'is_active': page==pageNum
            })
        });
    };

    var reset_results = function (results) {
        results.pagination = {};
        results.rows = [];
        results.pageBtnArray = [];
        results.pageNum = null;
        results.pageCount = null;
    }



    $location.search(queryCriteria);
    $scope.query(queryCriteria.page);
});