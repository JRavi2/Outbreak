window.onscroll = function() {
    scrollFunction();
};
function scrollFunction() {
    if (
        document.body.scrollTop > 100 ||
        document.documentElement.scrollTop > 100
    ) {
        document.getElementById("tops").style.height = "60px";
        document.getElementById("logo").style.fontSize = "20px";
    } else {
        document.getElementById("tops").style.height = "70px ";
        document.getElementById("logo").style.fontSize = "30px";
    }
}

function openPage() {
    document.getElementById("page").style.height = "100%";
    document.getElementById("contact").style.backgroundColor = "#ff7315";
    document.getElementById("home").style.backgroundColor = "white";
}
function closePage() {
    document.getElementById("page").style.height = "0%";
    document.getElementById("contact").style.backgroundColor = "white";
    document.getElementById("home").style.backgroundColor = "#ff7315";
}
function openAbout() {
    document.getElementById("pageAbout").style.height = "100%";
    document.getElementById("about").style.backgroundColor = "#ff7315";
    document.getElementById("home").style.backgroundColor = "white";
}
function closeAbout() {
    document.getElementById("pageAbout").style.height = "0%";
    document.getElementById("about").style.backgroundColor = "white";
    document.getElementById("home").style.backgroundColor = "#ff7315";
}
