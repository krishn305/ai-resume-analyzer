let file = null;

const dropZone = document.getElementById("drop-zone");

let gaugeChart = null;
let skillChart = null;


// Drag & Drop events
dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.style.background = "rgba(255,255,255,0.2)";
});

dropZone.addEventListener("dragleave", () => {
    dropZone.style.background = "transparent";
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    file = e.dataTransfer.files[0];
    dropZone.innerHTML = "Uploaded: " + file.name;
});


// Main analysis function
async function analyze() {

    if (!file) {
        alert("Please upload a resume first.");
        return;
    }

    const job = document.getElementById("job").value;

    const formData = new FormData();
    formData.append("resume", file);
    formData.append("job_description", job);

    try {

        document.getElementById("loader").classList.remove("hidden");

        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        document.getElementById("loader").classList.add("hidden");


        // ATS Score
        document.getElementById("scoreText").innerHTML =
            `ATS Score: ${data["ATS Score"]}`;


        // Missing Skills
        const missing = data["Missing Skills"] || [];
        document.getElementById("missingSkills").innerHTML =
            "<b>Missing Skills:</b> " + missing.join (", ")
            "<b>Missing Skills:</b None 👍👌"


        // Suggestions
        const suggestions = data["Suggestions"] || [];
        document.getElementById("suggestions").innerHTML =
            "<b>Suggestions:</b><br>" + suggestions.join("<br>");


        drawGauge(data["ATS Score"]);
        drawSkillChart(data["Detected Skills"]);

    } catch (error) {

        console.error(error);

        document.getElementById("loader").classList.add("hidden");

        alert("Error connecting to backend.");
    }
}


// ATS Gauge Chart
function drawGauge(score) {

    const ctx = document.getElementById("gauge");

    if (gaugeChart) {
        gaugeChart.destroy();
    }

    gaugeChart = new Chart(ctx, {

        type: "doughnut",

        data: {
            labels: ["Score", "Remaining"],
            datasets: [{
                data: [score, 100 - score],
                backgroundColor: ["#00f5ff", "#ffffff33"],
                borderWidth: 0
            }]
        },

        options: {
            rotation: 270,
            circumference: 180,
            cutout: "75%",
            plugins: {
                legend: { display: false }
            }
        }

    });
}


// Skill Chart
function drawSkillChart(skills) {

    const ctx = document.getElementById("skillsChart");

    if (skillChart) {
        skillChart.destroy();
    }

    skillChart = new Chart(ctx, {

        type: "bar",

        data: {
            labels: skills,
            datasets: [{
                label: "Detected Skills",
                data: skills.map(() => 100),
                backgroundColor: "#00f5ff"
            }]
        },

        options: {
            plugins: {
                legend: { display: false }
            }
        }

    });
}