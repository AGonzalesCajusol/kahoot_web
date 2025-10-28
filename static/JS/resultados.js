document.addEventListener("DOMContentLoaded", () => {
  const idCuestionario = window.idCuestionario || null;

  if (!idCuestionario) {
    console.error("❌ No se encontró el id del cuestionario.");
    return;
  }

  cargarResultados(idCuestionario);
});

async function cargarResultados(idCuestionario) {
  try {
    const response = await fetch(`/api/resultados/${idCuestionario}`);
    const data = await response.json();

    if (data.error) {
      mostrarError(data.error);
      return;
    }

    mostrarTop3(data.top3);
    mostrarTabla(data.participantes);
  } catch (error) {
    console.error("Error al obtener los resultados:", error);
    mostrarError("Error al cargar los resultados. Inténtalo más tarde.");
  }
}

function mostrarTop3(top3) {
  const topContainer = document.getElementById("top3-container");
  topContainer.innerHTML = "";

  if (!top3 || top3.length === 0) {
    topContainer.innerHTML = "<p class='text-center'>No hay resultados disponibles.</p>";
    return;
  }

  const medallas = ["1er Lugar", "2do Lugar", "3er Lugar"];
  const colores = ["#FFD700", "#C0C0C0", "#CD7F32"];

  top3.forEach((jugador, index) => {
    const avatarURL = `https://ui-avatars.com/api/?name=${jugador.alias}&background=0072ff&color=fff`;

    const col = document.createElement("div");
    col.classList.add("col-4", "text-center");
    col.innerHTML = `
      <img src="${avatarURL}" alt="Avatar" class="avatar mb-2">
      <h5>${jugador.alias}</h5>
      <p>${jugador.puntaje} Puntos</p>
      <div class="medal" style="color:${colores[index]}">
        <i class="bi bi-trophy-fill"></i> ${medallas[index]}
      </div>
    `;
    topContainer.appendChild(col);
  });
}

function mostrarTabla(participantes) {
  const tbody = document.querySelector("#tabla-resultados tbody");
  tbody.innerHTML = "";

  if (!participantes || participantes.length === 0) {
    tbody.innerHTML = `<tr><td colspan="3" class="text-center">No hay más participantes.</td></tr>`;
    return;
  }

  participantes.forEach((p, index) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${index + 4}</td>
      <td>${p.alias}</td>
      <td>${p.puntaje}</td>
    `;
    tbody.appendChild(row);
  });
}

function mostrarError(mensaje) {
  const container = document.querySelector(".quiz-container") || document.body;
  container.innerHTML = `
    <div class="alert alert-danger text-center mt-4">${mensaje}</div>
  `;
}

function exportToExcel() {
  const ws = XLSX.utils.table_to_sheet(document.querySelector("table"));
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, "Resultados");
  XLSX.writeFile(wb, "resultados_juego.xlsx");
}

function exportToDrive() {
  gapi.load("client:auth2", initClient);

  function initClient() {
    gapi.client
      .init({
        apiKey: "YOUR_API_KEY",
        clientId: "YOUR_CLIENT_ID",
        scope: "https://www.googleapis.com/auth/drive.file",
        discoveryDocs: ["https://www.googleapis.com/discovery/v1/apis/drive/v3/rest"],
      })
      .then(() => {
        gapi.auth2.getAuthInstance().signIn().then(uploadToDrive);
      });
  }

  function uploadToDrive() {
    const ws = XLSX.utils.table_to_sheet(document.querySelector("table"));
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Resultados");
    const fileContent = XLSX.write(wb, { bookType: "xlsx", type: "binary" });
    const file = new Blob([fileContent], {
      type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    });

    const metadata = {
      name: "resultados_juego.xlsx",
      mimeType: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    };

    const form = new FormData();
    form.append("metadata", new Blob([JSON.stringify(metadata)], { type: "application/json" }));
    form.append("file", file);

    fetch("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart", {
      method: "POST",
      headers: new Headers({
        Authorization: "Bearer " + gapi.auth2.getAuthInstance().currentUser.get().getAuthResponse().access_token,
      }),
      body: form,
    })
      .then((res) => res.json())
      .then((res) => console.log("Archivo subido:", res))
      .catch((err) => console.error("Error al subir:", err));
  }
}
