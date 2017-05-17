function login(userName, password, verifyCode) {
    var result = {};
    $.ajax({
        url: "http://localhost:8000/auth",
        type: "post",
        dataType: "json",
        beforeSend: function (request) {
            request.setRequestHeader("Access-Token", "123333");
        },
        success: function (data, status) {
            console.log(status)
            console.log(data)
        },
        error: function (err) {
            console.log(err)
        }
    });
    return result;
}

function getUser(userId) {
    var result = {};
    $.ajax({
        url: "http://localhost:8000/user/1",
        type: "get",
        dataType: "json",
        //beforeSend: function (request) {
        //    request.setRequestHeader("Access-Token", "123333");
        //},
        success: function (data, status) {
            result = data.result
        },
        error: function (err) {
            console.log(err)
        }
    });
    return result;
}