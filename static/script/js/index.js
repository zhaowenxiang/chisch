$(document).ready(function () {
    /*设置课程，讲师查询框的默认值跟样式*/
    var defaultSearchInputValue = "Search...";

    function setDefaultSearchInput(tag) {
        tag.val(defaultSearchInputValue).css("color", "#777")
    }
    function clearDefaultSearchInput(tag) {
        tag.val("").css("color", "#fff")
    }
    setDefaultSearchInput($("#searchInput"))
    $("#searchInput").focus(function () {
       if ($("#searchInput").val() == defaultSearchInputValue) {
           clearDefaultSearchInput($("#searchInput"))
       }
    });
    $("#searchInput").blur(function () {
       if ($("#searchInput").val() == "") {
           setDefaultSearchInput($("#searchInput"))
       }
    });
});