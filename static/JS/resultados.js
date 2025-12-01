let esDocenteOwner = false;

document.addEventListener("DOMContentLoaded", () => {
  const idCuestionario = window.idCuestionario || null;

  if (!idCuestionario) {
    mostrarError("No se encontró el ID del cuestionario.");
    return;
  }

  cargarResultados(idCuestionario);
});

async function cargarResultados(idCuestionario) {
  try {
    const response = await fetch(`/api/resultados/${idCuestionario}`);
    
    if (!response.ok) {
      throw new Error(`Error HTTP: ${response.status}`);
    }
    
    const data = await response.json();

    if (data.error) {
      mostrarError(data.error);
      return;
    }

    esDocenteOwner = data.es_docente_dueño === true;

    mostrarEstadisticas(data.quiz);
    mostrarTop3(data.top3);
    mostrarParticipantes(data.participantes);
    mostrarBotonRecompensa(data.usuario_actual, data.quiz);
    mostrarBotonRecompensasDocente(data.es_docente_dueño, data.quiz);
  } catch (error) {
    mostrarError("Error al cargar los resultados. Inténtalo más tarde.");
  }
}

async function mostrarEstadisticas(quiz) {
  const estadisticasContainer = document.getElementById("estadisticas-container");
  if (!estadisticasContainer) return;

  const totalParticipantes = quiz?.total_participantes || 0;
  const puntajeMaximo = quiz?.puntaje_maximo || 0;
  
  // Si es docente, mostrar sumatoria total de puntos de recompensa
  // Si es jugador, mostrar sus puntos de recompensa
  let puntosRecompensa = 0;
  if (esDocenteOwner) {
    // Docente: mostrar sumatoria total de todos los puntos de recompensa
    puntosRecompensa = quiz?.total_puntos_recompensa || 0;
  } else {
    // Jugador: obtener sus puntos de recompensa
    try {
      const idCuestionario = window.idCuestionario;
      if (idCuestionario) {
        const response = await fetch(`/api/puntos_recompensa_jugador/${idCuestionario}`);
        if (response.ok) {
          const data = await response.json();
          puntosRecompensa = data.puntos_recompensa || 0;
          console.log('Puntos de recompensa obtenidos:', puntosRecompensa);
        } else {
          console.error('Error en la respuesta de la API:', response.status, response.statusText);
        }
      } else {
        console.error('No se encontró idCuestionario');
      }
    } catch (error) {
      console.error('Error al obtener puntos de recompensa:', error);
    }
  }

  estadisticasContainer.innerHTML = `
    <div class="stat-card">
      <i class="bi bi-people-fill"></i>
      <div class="stat-info">
        <h3>${totalParticipantes}</h3>
        <p>Participantes</p>
      </div>
    </div>
    <div class="stat-card">
      <i class="bi bi-star-fill"></i>
      <div class="stat-info">
        <h3>${Number(puntajeMaximo).toFixed(2).replace(/\.?0+$/, '')}</h3>
        <p>Puntaje Máximo</p>
      </div>
    </div>
    <div class="stat-card">
      <i class="bi bi-trophy-fill"></i>
      <div class="stat-info">
        <h3>${puntosRecompensa}</h3>
        <p>${esDocenteOwner ? 'Total Puntos de Recompensa' : 'Puntos de Recompensa'}</p>
      </div>
    </div>
  `;
}

function mostrarTop3(top3) {
  const podioContainer = document.getElementById("podio-container");
  if (!podioContainer) return;

  podioContainer.innerHTML = "";

  if (!top3 || top3.length === 0) {
    podioContainer.innerHTML = `
      <div class="no-results" style="text-align: center; padding: 3rem; color: rgba(255, 255, 255, 0.8);">
        <i class="bi bi-inbox" style="font-size: 4rem; margin-bottom: 1rem; display: block;"></i>
        <p style="font-size: 1.2rem;">No hay resultados disponibles todavía.</p>
      </div>
    `;
    return;
  }

  const medallas = ["🥇", "🥈", "🥉"];
  const posiciones = ["1er Lugar", "2do Lugar", "3er Lugar"];

  top3.forEach((jugador, index) => {
    // Obtener iniciales para el avatar
    const iniciales = jugador.alias ? jugador.alias.substring(0, 2).toUpperCase() : "??";
    const avatarURL = `https://ui-avatars.com/api/?name=${encodeURIComponent(jugador.alias || 'Usuario')}&background=0072ff&color=fff&size=200&bold=true&font-size=0.5`;
    
    const podioItem = document.createElement("div");
    podioItem.className = `podio-item podio-${index + 1}`;
    
    // Agregar clase especial para el ganador (primer lugar)
    if (index === 0) {
      podioItem.classList.add('ganador');
    }
    
    podioItem.innerHTML = `
      ${index === 0 ? '<div class="ganador-badge">🏆 GANADOR 🏆</div>' : ''}
      <div class="medalla-podio">${medallas[index]}</div>
      <div class="avatar-podio">
        <img src="${avatarURL}" alt="${jugador.alias}" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
        <div style="display: none; width: 100%; height: 100%; align-items: center; justify-content: center; font-size: 3rem; font-weight: 900; color: #fff; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">${iniciales}</div>
      </div>
      <div class="info-podio">
        <h3>${jugador.alias || 'Sin alias'}</h3>
        <span class="puntaje-podio">${Number(jugador.puntaje || 0).toFixed(2).replace(/\.?0+$/, '')} pts</span>
        <span class="posicion-podio">${posiciones[index]}</span>
      </div>
      ${index === 0 ? '<div class="confetti-container"></div>' : ''}
    `;
    
    podioContainer.appendChild(podioItem);
    
    // Si es el ganador, activar animaciones especiales después de un pequeño delay
    if (index === 0) {
      setTimeout(() => {
        podioItem.classList.add('ganador-activo');
        crearConfeti(podioItem);
      }, 500);
    }
  });
}

function crearConfeti(container) {
  const confettiContainer = container.querySelector('.confetti-container');
  if (!confettiContainer) return;
  
  const colors = ['#FFD700', '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F'];
  const confettiCount = 50;
  
  for (let i = 0; i < confettiCount; i++) {
    const confetti = document.createElement('div');
    confetti.className = 'confetti-piece';
    confetti.style.left = Math.random() * 100 + '%';
    confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
    confetti.style.animationDelay = Math.random() * 2 + 's';
    confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
    confettiContainer.appendChild(confetti);
  }
  
  // Limpiar confeti después de la animación
  setTimeout(() => {
    confettiContainer.innerHTML = '';
  }, 5000);
}

function mostrarParticipantes(participantes) {
  const participantesContainer = document.getElementById("participantes-container");
  if (!participantesContainer) return;

  participantesContainer.innerHTML = "";

  if (!participantes || participantes.length === 0) {
    participantesContainer.innerHTML = `
      <div class="no-results">
        <i class="bi bi-info-circle"></i>
        <p>No hay más participantes en la clasificación.</p>
      </div>
    `;
    return;
  }

  participantes.forEach((p, index) => {
    const posicion = index + 4;
    const iniciales = p.alias ? p.alias.substring(0, 2).toUpperCase() : "??";
    const avatarURL = `https://ui-avatars.com/api/?name=${encodeURIComponent(p.alias || 'Usuario')}&background=6c757d&color=fff&size=120&bold=true&font-size=0.4`;
    
    const participanteItem = document.createElement("div");
    participanteItem.className = "participante-item";
    
    participanteItem.innerHTML = `
      <div class="posicion-numero">${posicion}</div>
      <div class="avatar-participante">
        <img src="${avatarURL}" alt="${p.alias}" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
        <div style="display: none; width: 100%; height: 100%; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: 900; color: #fff; background: linear-gradient(135deg, #6c757d 0%, #5a6268 100%);">${iniciales}</div>
      </div>
      <div class="info-participante">
        <h4>${p.alias || 'Sin alias'}</h4>
        <span class="puntaje-participante">${Number(p.puntaje || 0).toFixed(2).replace(/\.?0+$/, '')} puntos</span>
      </div>
    `;
    
    participantesContainer.appendChild(participanteItem);
  });
}

function mostrarError(mensaje) {
  const container = document.querySelector(".resultados-container") || document.body;
  container.innerHTML = `
    <div class="alert alert-danger text-center mt-4 p-4">
      <i class="bi bi-exclamation-triangle-fill"></i>
      <h3>Error</h3>
      <p>${mensaje}</p>
    </div>
  `;
}


function puedeEjecutarAccionDocente() {
  if (!esDocenteOwner) {
    Swal.fire({
      icon: 'warning',
      title: 'Acceso restringido',
      text: 'Solo el docente puede realizar esta acción.',
      confirmButtonColor: '#667eea'
    });
    return false;
  }
  return true;
}

function exportarExcel() {
  if (!puedeEjecutarAccionDocente()) {
    return;
  }
  
  try {
    const idCuestionario = window.idCuestionario;
    
    // Obtener datos del podio
    const podioItems = document.querySelectorAll(".podio-item");
    const participanteItems = document.querySelectorAll(".participante-item");
    
    const datos = [];
    // Encabezados
    datos.push(["Posición", "Alias", "Puntaje"]);
    
    // Agregar top 3
    podioItems.forEach((item, index) => {
      const alias = item.querySelector(".info-podio h3")?.textContent?.trim() || "";
      const puntaje = item.querySelector(".puntaje-podio")?.textContent?.replace(" pts", "").trim() || "0";
      datos.push([index + 1, alias, parseFloat(puntaje) || 0]);
    });
    
    // Agregar resto de participantes
    let posicionActual = 4;
    participanteItems.forEach((item) => {
      const posicion = item.querySelector(".posicion-numero")?.textContent?.trim() || posicionActual;
      const alias = item.querySelector(".info-participante h4")?.textContent?.trim() || "";
      const puntaje = item.querySelector(".puntaje-participante")?.textContent?.replace(" puntos", "").trim() || "0";
      datos.push([posicion, alias, parseFloat(puntaje) || 0]);
      posicionActual++;
    });
    
    // Crear workbook
    const ws = XLSX.utils.aoa_to_sheet(datos);
    
    // Ajustar ancho de columnas
    ws['!cols'] = [
      { wch: 10 }, // Posición
      { wch: 30 }, // Alias
      { wch: 15 }  // Puntaje
    ];
    
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Resultados");
    
    // Generar nombre de archivo con fecha
    const fecha = new Date().toISOString().split('T')[0];
    const nombreArchivo = `resultados_cuestionario_${idCuestionario}_${fecha}.xlsx`;
    
    // Descargar archivo
    XLSX.writeFile(wb, nombreArchivo);
    
    Swal.fire({
      icon: 'success',
      title: '¡Exportado!',
      text: 'Los resultados se han descargado correctamente.',
      timer: 2000,
      showConfirmButton: false,
      confirmButtonColor: '#667eea'
    });
  } catch (error) {
    console.error('Error al exportar:', error);
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'No se pudo exportar el archivo. Inténtalo de nuevo.',
      confirmButtonColor: '#667eea'
    });
  }
}

function guardarEnGoogleDrive() {
  if (!puedeEjecutarAccionDocente()) {
    return;
  }
  
  Swal.fire({
    icon: 'info',
    title: 'Guardar en Google Drive',
    html: `
      <div style="text-align: left; padding: 1rem;">
        <p style="margin-bottom: 1rem;"><strong>Instrucciones:</strong></p>
        <ol style="padding-left: 1.5rem; line-height: 1.8;">
          <li>Primero, exporta los resultados a Excel usando el botón "Exportar a Excel"</li>
          <li>Abre tu <a href="https://drive.google.com" target="_blank" style="color: #4285f4;">Google Drive</a></li>
          <li>Haz clic en "Nuevo" → "Subir archivo"</li>
          <li>Selecciona el archivo Excel descargado</li>
          <li>¡Listo! El archivo estará en tu Google Drive</li>
        </ol>
      </div>
    `,
    confirmButtonText: 'Entendido',
    confirmButtonColor: '#4285F4',
    width: '500px'
  });
}

function guardarEnOneDrive() {
  if (!puedeEjecutarAccionDocente()) {
    return;
  }
  
  Swal.fire({
    icon: 'info',
    title: 'Guardar en OneDrive',
    html: `
      <div style="text-align: left; padding: 1rem;">
        <p style="margin-bottom: 1rem;"><strong>Instrucciones:</strong></p>
        <ol style="padding-left: 1.5rem; line-height: 1.8;">
          <li>Primero, exporta los resultados a Excel usando el botón "Exportar a Excel"</li>
          <li>Abre tu <a href="https://onedrive.live.com" target="_blank" style="color: #0078d4;">OneDrive</a></li>
          <li>Haz clic en "Subir" → "Archivos"</li>
          <li>Selecciona el archivo Excel descargado</li>
          <li>¡Listo! El archivo estará en tu OneDrive</li>
        </ol>
      </div>
    `,
    confirmButtonText: 'Entendido',
    confirmButtonColor: '#0078D4',
    width: '500px'
  });
}

function volverDashboard() {
  window.location.href = '/dashboard';
}

function puedeEjecutarAccionDocente() {
  if (!esDocenteOwner) {
    Swal.fire({
      icon: 'warning',
      title: 'Acción no disponible',
      text: 'Solo el docente puede realizar esta acción.'
    });
    return false;
  }
  return true;
}

function mostrarBotonRecompensa(usuario_actual, quiz) {
  // Ya no se muestra el botón de recibir recompensa, las recompensas se otorgan automáticamente
  return;
}

function mostrarBotonRecompensasDocente(es_docente_dueño, quiz) {
  // Solo mostrar el botón si es docente dueño del cuestionario
  if (!es_docente_dueño) {
    return;
  }
  
  const accionesSection = document.querySelector('.acciones-section');
  if (!accionesSection) return;

  // Mostrar grupo de exportaciones
  const exportContainer = document.getElementById('acciones-export');
  if (exportContainer) {
    exportContainer.style.display = 'flex';
  }
  
  // Verificar si ya existe el botón
  if (document.getElementById('btn-recompensas-docente')) {
    return;
  }
  
  // Crear botón para ver recompensas
  const botonRecompensas = document.createElement('button');
  botonRecompensas.id = 'btn-recompensas-docente';
  botonRecompensas.className = 'btn-accion';
  botonRecompensas.style.cssText = 'background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none;';
  botonRecompensas.innerHTML = '<i class="bi bi-gift"></i> Ver Recompensas Otorgadas';
  botonRecompensas.onclick = () => {
    const idCuestionario = window.idCuestionario;
    window.location.href = `/recompensas_cuestionario/${idCuestionario}`;
  };
  
  // Insertar antes del botón "Volver al Dashboard"
  const btnVolver = accionesSection.querySelector('.btn-volver');
  if (btnVolver) {
    btnVolver.parentElement.insertBefore(botonRecompensas, btnVolver);
  } else {
    accionesSection.querySelector('.container').appendChild(botonRecompensas);
  }
}
