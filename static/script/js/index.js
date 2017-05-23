$(document).ready(function () {
    $("#nav-table td").click(function () {
        console.log(window.location.href);
        console.log(window.location.hash)
        $(this).siblings().removeClass("header-nav-td-select");
        $(this).addClass("header-nav-td-select");
        var id = "#" + $(this).attr("id")
        console.log(id);
        $("." + $(this).attr("id") + "-nav").show()
    });



    $("#find-video").click()
});
