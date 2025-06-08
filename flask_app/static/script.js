document.addEventListener("DOMContentLoaded", () => {
    const infoList = document.getElementById("infoList");
    const infoForm = document.getElementById("infoForm");

    function loadInfos() {
        fetch("/api/steps")
            .then(response => response.json())
            .then(infos => {
                infoList.innerHTML = "";
                infos.forEach(info => {
                    const li = document.createElement("li");
                    li.innerHTML = `${info.steps} (${info.date}) 
                        <button onclick="deleteInfo(${info.id})">❌</button>`;
                    infoList.appendChild(li);
                    let total = infos.reduce((sum, info) => sum + info.steps, 0);
                    document.getElementById("totalCell").textContent = total;
                });
            });
    }

    infoForm.addEventListener("submit", event => {
        event.preventDefault();
        const steps = document.getElementById("steps").value;
        const date = document.getElementById("date").value;

        fetch("/api/steps", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ steps, date })
        }).then(response => response.json())
          .then(() => {
              infoForm.reset();
              loadInfos();
          });
    });

    window.deleteInfo = (id) => {
        fetch(`/api/steps/${id}`, { method: "DELETE" })
            .then(() => loadInfos());
    };

    loadInfos();
});
