// Выделение пунктов меню при наведении
$(".menu_conteiner li:not(.active)").mouseenter(function () {
    $(this).addClass("active");
}).mouseleave(function () {
    $(this).removeClass("active");
});
// Анимация изображений при наведении
$(".one").hover(
                function() {
                    $(this).animate({
                        width: "530px",
                        height: "386px",

                    }, "slow");
                }, function() {
                    $(this).animate({
                        width: "510px",
                        height: "366px",

                    }, "slow");
                });
                $(".two").hover(
                function() {
                    $(this).animate({
                        width: "560px",
                        height: "416px",

                    }, "slow");
                }, function() {
                    $(this).animate({
                        width: "540px",
                        height: "396px",

                    }, "slow");
                });