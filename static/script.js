let currentMode = "Beginner";

// Switch Beginner / Advanced mode
function selectMode(mode){
    currentMode = mode;
    document.getElementById("selectedMode").innerText = mode;
    document.getElementById("beginnerTab").classList.toggle("active", mode === "Beginner");
    document.getElementById("advancedTab").classList.toggle("active", mode === "Advanced");
}

// Call backend to explain code
async function explainCode() {
    const code = document.getElementById("codeInput").value;
    if(!code){
        alert("Please paste some code first!");
        return;
    }

    document.getElementById("loader").style.display = "block";
    document.getElementById("output").innerText = "";

    try {
        const response = await fetch("/explain", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({code: code, mode: currentMode})
        });

        if(!response.ok) throw new Error(`Server responded with ${response.status}`);

        const data = await response.json();
        document.getElementById("output").innerText = data.explanation;
        document.getElementById("preview").textContent = code;
        Prism.highlightAll();
    } catch (error) {
        document.getElementById("output").innerText = "Error connecting to server.\n" + error;
        console.error(error);
    }

    document.getElementById("loader").style.display = "none";
}

// Copy explanation to clipboard
function copyExplanation(){
    const text = document.getElementById("output").innerText;
    navigator.clipboard.writeText(text);
    alert("Explanation copied!");
}

// Copy code preview to clipboard
function copyCode(){
    const code = document.getElementById("preview").innerText;
    navigator.clipboard.writeText(code);
    alert("Code copied!");
}