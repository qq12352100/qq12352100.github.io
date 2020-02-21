/**
 * Created by Administrator on 2017/4/7.
 */
$(document).ready(function() {
    $(document).scroll(function () {
        var scrollTop = $(document).scrollTop();
        var sp = $(".banner").outerHeight(true);
        if (scrollTop > sp) {
            $(".nav").css({"background": "rgba(0,0,0,0.7)"});
        }
        if (scrollTop < sp) {
            $(".nav").css({"background": "rgba(0,0,0,0)"});
        }
    });
	//nav 二级菜单
    $(".nav .ul1 .list1").mouseover(function(){
        $(".nav .list1 ul").stop().slideDown(500);
    }).mouseleave(function(){
        $(".nav .list1 ul").stop().slideUp(500);
    });

    //banner文字的动画
    $(".banner p").animate({"top":"180px", "opacity": "1"},1200);

    //关于微信
    $(".guanyu .guanyu-content ul li").mouseover(function(){
        $(this).find("p").css({"display":"block"});
    }).mouseleave(function(){
        $(this).find("p").css({"display":"none"});
    });

    $(".guanyu .guanyu-content ul li span").mouseover(function(){
        $(this).parent().prev().css({"transform":"scale(1.2)","transition":"all 500ms linear"});
    }).mouseout(function(){
        $(this).parent().prev().css({"transform":"scale(1)","transition":"all 500ms linear"});
    });


    //返回顶部
    function getscrollTop(){
        var scrollTop=0;
        if(document.documentElement&&document.documentElement.scrollTop){
            scrollTop=document.documentElement.scrollTop;
        }
        else if(document.body){
            scrollTop=document.body.scrollTop;
        }
        return scrollTop;
    }

    window.onscroll=function() {
        var top = document.getElementById("ruturn_top");
        if (getscrollTop() > 200) {
            top.style.display = "block";
        }
        if (getscrollTop() < 200 || getscrollTop() > 3800) {
            top.style.display = "none";
        }
    };

    $(".ruturn_top").click(function() {
        $("html, body").animate({ scrollTop: 0 }, 1000);
    });
});