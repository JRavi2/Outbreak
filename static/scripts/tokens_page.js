const departments = document.getElementsByClassName("departments");
const decrLinks = document.getElementsByClassName("decr-tokens");
const incrLinks = document.getElementsByClassName("incr-tokens");
// console.log(incrLinks);
const increaseTokens = e => {
    e.preventDefault();
    fetch("incr-tokens/" + e.currentTarget.dept + "/");
};

const decreaseTokens = e => {
    e.preventDefault();
    fetch("decr-tokens/" + e.currentTarget.dept + "/");
};

for (var i = 0; i < decrLinks.length; i++) {
    decrLinks[i].dept = departments[i].innerHTML;
    decrLinks[i].addEventListener("click", decreaseTokens);
    incrLinks[i].dept = departments[i].innerHTML;
    incrLinks[i].addEventListener("click", increaseTokens);
}
