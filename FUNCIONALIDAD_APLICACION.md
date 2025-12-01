# Funcionalidad de la Aplicación Web GoQuiz

## Descripción General

**GoQuiz** es una aplicación web educativa tipo Kahoot que permite a los docentes crear cuestionarios interactivos y a los estudiantes participar en juegos de preguntas y respuestas en tiempo real. La aplicación soporta dos modalidades de juego: **Individual** y **Grupal**, con un sistema de recompensas y seguimiento de resultados.

---

## Arquitectura del Sistema

La aplicación está desarrollada con:
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Base de Datos**: MySQL
- **Comunicación en Tiempo Real**: Socket.IO
- **Autenticación**: JWT (JSON Web Tokens) y Sesiones

---

## CRUDs por Integrante (4 Integrantes)

La aplicación implementa **4 CRUDs principales**, cada uno desarrollado por un integrante del equipo:

### 1. CRUD de DOCENTE
**Responsable: Integrante 1**

Gestiona la información de los docentes del sistema.

#### Funcionalidades:
- **Create (Crear)**: Registro de nuevos docentes con validación de correo único
- **Read (Leer)**: 
  - Obtener docente por ID
  - Obtener docente por correo
  - Listar todos los docentes
- **Update (Actualizar)**: Modificación de datos del docente (correo, contraseña, nombres, apellidos)
- **Delete (Eliminar)**: Eliminación de docentes del sistema

#### Endpoints API:
- `POST /api_registrar_docente` - Registrar nuevo docente
- `POST /api_actualizar_docente` - Actualizar docente existente
- `GET /api_obtener_docente_id` - Obtener docente por ID
- `GET /api_obtener_docentes` - Listar todos los docentes
- `DELETE /api_eliminar_docente` - Eliminar docente

#### Características:
- Encriptación de contraseñas con SHA-256
- Validación de correo único (no puede duplicarse con jugadores)
- Gestión de sesiones de docente
- Autenticación JWT

---

### 2. CRUD de JUGADOR
**Responsable: Integrante 2**

Gestiona la información de los jugadores/estudiantes del sistema.

#### Funcionalidades:
- **Create (Crear)**: Registro de nuevos jugadores con validación de email único
- **Read (Leer)**:
  - Obtener jugador por ID
  - Obtener jugador por email
  - Listar todos los jugadores
  - Obtener cuestionarios jugados por un jugador
- **Update (Actualizar)**: Modificación de datos del jugador (email, contraseña)
- **Delete (Eliminar)**: Eliminación de jugadores del sistema

#### Endpoints API:
- `POST /api_registrar_jugador` - Registrar nuevo jugador
- `POST /api_actualizar_jugador` - Actualizar jugador existente
- `GET /api_obtener_jugador_id` - Obtener jugador por ID
- `GET /api_obtener_jugadores` - Listar todos los jugadores
- `DELETE /api_eliminar_jugador` - Eliminar jugador

#### Características:
- Encriptación de contraseñas con SHA-256
- Validación de email único
- Seguimiento de cuestionarios jugados
- Sistema de puntos de recompensa (máximo 1000 puntos)
- Gestión de sesiones de jugador

---

### 3. CRUD de CUESTIONARIO
**Responsable: Integrante 3**

Gestiona la creación, modificación y administración de cuestionarios.

#### Funcionalidades:
- **Create (Crear)**: 
  - Crear cuestionarios individuales o grupales
  - Importar cuestionarios desde Excel
  - Generar PIN único automáticamente
  - Subir imágenes para cuestionarios
- **Read (Leer)**:
  - Obtener cuestionario por ID
  - Listar cuestionarios activos de un docente
  - Listar cuestionarios archivados
  - Obtener datos completos del cuestionario (preguntas y alternativas)
  - Validar PIN de acceso
- **Update (Actualizar)**: 
  - Modificar datos del cuestionario (nombre, descripción, tipo, estado, imagen)
  - Agregar preguntas a cuestionarios existentes
  - Modificar preguntas y alternativas
  - Resetear cuestionario (generar nuevo PIN, limpiar participantes)
- **Delete (Eliminar)**: 
  - Eliminar cuestionario completo (incluye preguntas, alternativas, participantes, grupos, recompensas)

#### Endpoints API:
- `POST /api_registrar_cuestionario` - Registrar nuevo cuestionario
- `POST /api_actualizar_cuestionario` - Actualizar cuestionario existente
- `GET /api_obtener_cuestionario_id` - Obtener cuestionario por ID
- `GET /api_obtener_cuestionarios` - Listar cuestionarios
- `DELETE /api_eliminar_cuestionario` - Eliminar cuestionario

#### Características:
- Dos tipos de cuestionarios: **Individual (I)** y **Grupal (G)**
- Estados: **Público (P)** y **Privado (R)**
- Estados de juego: **Sin Iniciar (SL)**, **Iniciado (IN)**, **Finalizado (FN)**
- PIN único de 5 dígitos para acceso
- Importación masiva desde Excel
- Repositorio público de cuestionarios
- Reutilización de cuestionarios de otros docentes
- Gestión de imágenes

---

### 4. CRUD de GRUPO
**Responsable: Integrante 4**

Gestiona la formación y administración de grupos para cuestionarios grupales.

#### Funcionalidades:
- **Create (Crear)**: 
  - Crear grupos para cuestionarios grupales
  - Asignar líder del grupo
  - Establecer método de evaluación (votación, consenso, líder)
- **Read (Leer)**:
  - Obtener grupo por ID
  - Listar todos los grupos de un cuestionario
  - Obtener grupos disponibles para unirse
  - Obtener miembros de un grupo
  - Obtener grupo al que pertenece un participante
- **Update (Actualizar)**: 
  - Actualizar datos del grupo (nombre, método de evaluación)
  - Agregar miembros al grupo (máximo 5 miembros)
  - Unirse a un grupo existente
- **Delete (Eliminar)**: 
  - Eliminar grupo completo
  - Salir de un grupo (miembros)
  - Disolver grupo (líder)

#### Endpoints API:
- `POST /api_registrar_grupo` - Crear nuevo grupo
- `POST /api_actualizar_grupo` - Actualizar grupo existente
- `GET /api_obtener_grupo_id` - Obtener grupo por ID
- `GET /api_obtener_grupos` - Listar grupos
- `DELETE /api_eliminar_grupo` - Eliminar grupo

#### Características:
- Límite de 5 miembros por grupo
- Sistema de líder (quien crea el grupo)
- Métodos de evaluación:
  - **Votación**: Decisión por mayoría
  - **Consenso**: Decisión unánime
  - **Líder**: El líder decide
- Gestión de miembros (agregar, eliminar)
- Estados: **Activo (A)**, **Disuelto (D)**

---

## Funcionalidades Adicionales del Sistema

### Sistema de Preguntas y Alternativas
- **Preguntas**: Soporta dos tipos:
  - **Verdadero/Falso (VF)**: 2 alternativas fijas
  - **Alternativa Múltiple (ALT)**: 2-6 alternativas
- Puntaje configurable por pregunta (1-1000 puntos)
- Tiempo de respuesta configurable (2-300 segundos)
- Validación de respuesta correcta

### Sistema de Participantes
- Registro de participantes con alias único por cuestionario
- Participantes anónimos (sin cuenta) o registrados
- Seguimiento de puntajes individuales
- Sala de espera antes de iniciar el juego

### Sistema de Respuestas
- **Respuestas Individuales**: Para cuestionarios individuales
- **Respuestas Grupales**: Para cuestionarios grupales
- Registro de tiempo utilizado por respuesta
- Cálculo automático de puntajes

### Sistema de Recompensas
- Otorgamiento automático según posición en el ranking
- Sistema de puntos:
  - Top 1: 100 puntos
  - Top 2: 75 puntos
  - Top 3: 50 puntos
  - Top 10%: 25 puntos
  - Resto: 10 puntos
- Límite máximo de 1000 puntos acumulados
- Historial de recompensas por jugador

### Sistema de Juego en Tiempo Real
- Inicio y control del juego por el docente
- Sincronización de preguntas con Socket.IO
- Contador de tiempo en tiempo real
- Actualización de ranking en vivo
- Finalización automática del juego

### Sistema de Resultados
- Visualización de resultados al finalizar el juego
- Ranking de participantes ordenado por puntaje
- Estadísticas de tiempo utilizado
- Exportación de resultados

### Autenticación y Seguridad
- Autenticación JWT para APIs
- Sesiones para la aplicación web
- Decoradores de autenticación (`@requiere_login`, `@requiere_docente`)
- Encriptación de contraseñas con SHA-256
- Validación de permisos por rol

### Importación y Exportación
- Importación de cuestionarios desde Excel
- Plantilla Excel descargable
- Validación de formato Excel
- Procesamiento de errores en importación

---

## Flujo de Uso de la Aplicación

### Para Docentes:
1. **Registro/Login**: Crear cuenta o iniciar sesión
2. **Crear Cuestionario**: 
   - Manualmente desde la interfaz
   - Importar desde Excel
   - Reutilizar de repositorio público
3. **Configurar**: Agregar preguntas, alternativas, configurar tipo y estado
4. **Iniciar Juego**: Generar PIN y compartir con estudiantes
5. **Monitorear**: Ver participantes en sala de espera
6. **Controlar**: Iniciar, pausar o finalizar el juego
7. **Resultados**: Ver ranking y estadísticas al finalizar

### Para Estudiantes/Jugadores:
1. **Acceso**: Ingresar PIN del cuestionario
2. **Registro**: Crear alias único para el cuestionario
3. **Sala de Espera**: Esperar a que el docente inicie el juego
4. **Formar Grupo** (si es grupal): Crear o unirse a un grupo
5. **Jugar**: Responder preguntas en tiempo real
6. **Resultados**: Ver ranking y puntaje obtenido
7. **Recompensas**: Recibir puntos según posición

---

## Tecnologías y Herramientas Utilizadas

- **Backend**: Python 3.x, Flask, Flask-SocketIO, Flask-JWT
- **Base de Datos**: MySQL (PyMySQL)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5
- **Comunicación**: Socket.IO para tiempo real
- **Validación**: Validaciones en backend y frontend
- **Seguridad**: JWT, encriptación SHA-256, sesiones seguras

---

## Estructura del Proyecto

```
kahoot_web/
├── controladores/      # Lógica de negocio
│   ├── docente.py      # CRUD Docente
│   ├── jugador.py      # CRUD Jugador
│   ├── cuestionario.py # CRUD Cuestionario
│   ├── grupo.py        # CRUD Grupo
│   └── ...
├── routes/             # Rutas y endpoints
│   ├── api_todas_tablas.py  # APIs REST
│   ├── cuestionario.py
│   ├── grupo.py
│   └── ...
├── templates/          # Plantillas HTML
├── static/            # Archivos estáticos (CSS, JS, imágenes)
├── sql/               # Scripts SQL
├── modelos.py         # Clases del dominio
└── main.py            # Aplicación principal
```

---

## Conclusión

GoQuiz es una aplicación web completa que permite a los docentes crear y gestionar cuestionarios interactivos, y a los estudiantes participar en juegos educativos en tiempo real. El sistema está organizado en 4 CRUDs principales (Docente, Jugador, Cuestionario y Grupo), cada uno desarrollado por un integrante del equipo, garantizando una distribución equitativa del trabajo y una arquitectura modular y escalable.










