// DARK MODE TOGGLE

function toggleMode(){

    document.body.classList.toggle("dark-mode");

    if(localStorage.getItem("theme") === "dark"){
        localStorage.setItem("theme","light");
    } else {
        localStorage.setItem("theme","dark");
    }
}

// LOAD SAVED MODE

window.onload = function(){

    if(localStorage.getItem("theme") === "dark"){
        document.body.classList.add("dark-mode");
    }

}