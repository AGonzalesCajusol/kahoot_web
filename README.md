# GoQuiz - Aplicación Web Educativa

Aplicación web tipo Kahoot para crear y gestionar cuestionarios interactivos en tiempo real.

## Descripción

GoQuiz es una plataforma educativa que permite a los docentes crear cuestionarios interactivos y a los estudiantes participar en juegos de preguntas y respuestas. Soporta modalidades individuales y grupales, con sistema de recompensas y seguimiento de resultados.

## Características Principales

- ✅ CRUD de Docente (Gestión de docentes)
- ✅ CRUD de Jugador (Gestión de estudiantes)
- ✅ CRUD de Cuestionario (Creación y administración de cuestionarios)
- ✅ CRUD de Grupo (Formación y gestión de grupos)
- 🎮 Juego en tiempo real con Socket.IO
- 🏆 Sistema de recompensas y ranking
- 📊 Resultados y estadísticas
- 📥 Importación desde Excel
- 🔐 Autenticación JWT y sesiones

## Tecnologías

- **Backend**: Python, Flask, Flask-SocketIO
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Base de Datos**: MySQL
- **Autenticación**: JWT (JSON Web Tokens)

## Documentación Completa

Para una explicación detallada de la funcionalidad de la aplicación y los CRUDs por integrante, consulta el archivo [FUNCIONALIDAD_APLICACION.md](FUNCIONALIDAD_APLICACION.md).

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual: `python -m venv .venv`
3. Activar entorno virtual
4. Instalar dependencias: `pip install -r requirements.txt`
5. Configurar base de datos en `conexion.py`
6. Ejecutar: `python main.py`

## Estructura del Proyecto

- `controladores/` - Lógica de negocio (CRUDs)
- `routes/` - Rutas y endpoints
- `templates/` - Plantillas HTML
- `static/` - Archivos estáticos
- `modelos.py` - Clases del dominio
- `main.py` - Aplicación principal
