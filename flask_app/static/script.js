document.addEventListener("DOMContentLoaded", () => {
    const infoList = document.getElementById("infoList");
    const infoForm = document.getElementById("infoForm");

    // Функция загрузки списка пользователей
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
                });
            });
    }

    // Добавление пользователя
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

    // Удаление пользователя
    window.deleteInfo = (id) => {
        fetch(`/api/steps/${id}`, { method: "DELETE" })
            .then(() => loadInfos());
    };

    // Загрузка пользователей при загрузке страницы
    loadInfos();
});
