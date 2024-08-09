const bar = document.querySelector("#bar");
const close = document.querySelector("#close");
const nav = document.querySelector(".navbar");
const lists = document.querySelector("#lists");
// const body = document.querySelector("body");

// bar.addEventListener('click', () => {
//     nav.style.display ="block";
// });

close.addEventListener('click', () => {
    lists.classList.remove("active")
});

bar.addEventListener("click", () => (
    lists.classList.add("active")
));