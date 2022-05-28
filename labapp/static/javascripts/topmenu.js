// Выделяем пункт навигационного меню в зависимости от id элемента <main>

var main_id = document.querySelector("main").id;
var navmenu = document.getElementsByClassName("menu_conteiner")[0]
var navlist = navmenu.getElementsByTagName("li");
var headtext = document.getElementById("headname");
var menuelem;
var alerttext = "";

switch(main_id) {
	case 'Главная':
		menuelem = navlist[0];
		break;
	case 'О школе':
		menuelem = navlist[1];
		break;

	case 'Ученикам':
		menuelem = navlist[2];
		break;
	case 'Курсы':
		menuelem = navlist[3];
		break;

	default:
		menuelem = navlist[0];//??????
}
headtext.innerHTML = menuelem.innerHTML;
menuelem.classList.add("active");

    $(document).ready(function() {
$(".img-title p").hide();
$(".img-title h3").css("background-color", "rgb(253, 243, 238)","border-radius: 30px");
});
$(".img-title h3").click(function () {
$(this).next("p").hide("slow");
$(this).css("background-color", "rgb(253, 243, 238)", "border-radius: 30px");
});
$(".img-title h3").dblclick(function () {
$(this).next("p").show("slow");
$(this).css("background-color", "#e7e7e7");
});
/*function setHeaderText(elem) {
	var newheadtext = elem.innerHTML;
	var headtext = document.getElementById("headname");
	headtext.innerHTML = newheadtext;
	elem.parentNode.classList.add("active");
}*/