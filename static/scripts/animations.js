$(document).ready(function(){
    var partWidth = $(".part").width();
    var partHeight = $(".part").width();
        
    $(".part").mouseenter(function(){
        $(this).addClass("active");
        
        $('html, body').stop().delay(100).animate({
            scrollTop: $(this).offset().top
        }, 500);
        
        $(this).find(".heading").stop().delay(150).animate({
            top: "20%",
            left: "20%"
        }, 500);
        
        $(this).find(".docform").stop().delay(150).animate({
            opacity: 1
        }, 500);
        
    });
    
    $(".part").mouseleave(function(){
        $(this).removeClass("active");
        
        $(this).find(".heading").stop().delay(150).animate({
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)"
        }, 500);
        
        $(this).find(".docform").stop().delay(150).animate({
            opacity: 0
        }, 400);
    });
});