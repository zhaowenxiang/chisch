//简单的值对
define({
    color: "block",
    size: 'unisize',
});


//函数式定义
define(function () {
    return {
        color: "black",
        size: "unisize"
    }
});


define(function () {
    return {
        color: "black",
        size: "unisize"
    }
});

//存在依赖的函数式定义
define(["./cart", "./inventory"], function (cart, inventory) {
    return {
        color: "blue",
        size: "unsize",
        addToCart: function () {
            inventory.decrement(this);
            inventory.decrement(this);
        }
    }
});