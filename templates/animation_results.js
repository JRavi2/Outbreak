$(document).ready(function(){
    $(".card").each(function(){
        //alert("You clicked on a card");
        $(this).animate({
            opacity: 1,
            marginTop: "-=3px"
        }, 500);
    });
    //$(".card").each(function(){
    //    $(this).animate({
    //        transform: "translate(0%, 0%)"
    //    }, 200);
    //});
});