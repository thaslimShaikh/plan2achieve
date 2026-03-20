function toggleMode(){
    document.body.classList.toggle("dark-mode");

    if(localStorage.getItem("theme") === "dark"){
        localStorage.setItem("theme","light");
    } else {
        localStorage.setItem("theme","dark");
    }
}

window.onload = function(){

    if(localStorage.getItem("theme") === "dark"){
        document.body.classList.add("dark-mode");
    }

    setupMLSuggestion();
};


function setupMLSuggestion(){

    const goalInput = document.getElementById("goalInput");
    const suggestion = document.getElementById("mlSuggestion");
    const dropdown = document.getElementById("categorySelect");

    if(!goalInput || !suggestion || !dropdown) return;

    goalInput.addEventListener("input", async function(){

        const goal = goalInput.value;

        if(goal.length < 3){
            suggestion.innerText = "";
            return;
        }

        const res = await fetch(`/predict_category?goal=${goal}`);
        const data = await res.json();

        suggestion.innerText = "✨ Suggested: " + data.category;

        for(let option of dropdown.options){
            if(option.text.toLowerCase().includes(data.category.toLowerCase())){
                dropdown.value = option.text;
            }
        }
    });
}