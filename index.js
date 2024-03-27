// 获取外层ul
var outerList = document.getElementsByClassName('left_div')[0];
// 获取两层ul中的ul元素
var innerUlElements = outerList.querySelectorAll("ul ul");
// 遍历每个<ul>元素
innerUlElements.forEach(function(ulElement) {
    // 获取当前<ul>元素下的所有<li>元素
    var liElements = ulElement.getElementsByTagName('li');
    // 遍历并隐藏所有<li>元素
    for (var i = 0; i < liElements.length; i++) {
      liElements[i].classList.add('hidden');
    }
});
//隐藏或展示ul
function toggle_ul(ul) {
    var lis = ul.nextElementSibling.querySelectorAll("li");
    lis.forEach(function(liElement) {
        if (liElement.classList.contains('hidden')) {
            liElement.classList.remove('hidden');
        }else{
            liElement.classList.add('hidden');
        }
    });
}
//隐藏或展示左侧
function toggle_left_div() {
    var left_div = document.getElementsByClassName('left_div')[0];
    var rgith_div = document.getElementsByClassName('rgith_div')[0];
    if (left_div.classList.contains('hidden')) {
        left_div.classList.remove('hidden');
        rgith_div.style.width = 80+'%';
      } else {
        left_div.classList.add('hidden');
        rgith_div.style.width = 100+'%';
      }
}
