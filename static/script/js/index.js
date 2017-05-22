$(document).ready(function () {
    $(".headerNav td").click(function () {
       $(".headerNav td").removeClass("header_nav_select")
       $(this).addClass("header_nav_select");
    });

    $("#find_video_nav_ul li").click(function () {
       $("#find_video_nav_ul li").css("background", "none");
       $(this).css("background", "#111");
    });
});