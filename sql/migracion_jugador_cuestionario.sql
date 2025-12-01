-- ============================================
-- MIGRACIÓN: Eliminar Usuario, Participante, Participante_Cuestionario
-- Crear Jugador_Cuestionario
-- ============================================
-- IMPORTANTE: Este script eliminará datos existentes
-- Hacer backup antes de ejecutar
-- ============================================
-- NOTA: Si ves warnings sobre "Integer display width is deprecated",
-- es normal en MySQL 8.0+ y no afecta la funcionalidad.
-- Los warnings pueden ignorarse de forma segura.
-- ============================================

-- Paso 1: Eliminar Foreign Keys que dependen de Usuario
ALTER TABLE Respuesta DROP FOREIGN KEY IF EXISTS Respuesta_ibfk_1;
ALTER TABLE Recompensa DROP FOREIGN KEY IF EXISTS Recompensa_ibfk_2;
ALTER TABLE Grupo DROP FOREIGN KEY IF EXISTS Grupo_ibfk_2;
ALTER TABLE GrupoMiembro DROP FOREIGN KEY IF EXISTS GrupoMiembro_ibfk_2;
ALTER TABLE VotacionGrupo DROP FOREIGN KEY IF EXISTS VotacionGrupo_ibfk_3;

-- Paso 2: Eliminar las tablas antiguas
DROP TABLE IF EXISTS VotacionGrupo;
DROP TABLE IF EXISTS GrupoMiembro;
DROP TABLE IF EXISTS Grupo;
DROP TABLE IF EXISTS Respuesta;
DROP TABLE IF EXISTS Recompensa;
DROP TABLE IF EXISTS Participante_Cuestionario;
DROP TABLE IF EXISTS Participante;
DROP TABLE IF EXISTS Usuario;

-- Paso 3: Crear la nueva tabla Jugador_Cuestionario
CREATE TABLE IF NOT EXISTS Jugador_Cuestionario (
    id_jugador_cuestionario INT AUTO_INCREMENT,
    id_jugador INT DEFAULT NULL,
    id_cuestionario INT NOT NULL,
    alias VARCHAR(20) NOT NULL,
    puntaje DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    fecha_participacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_jugador_cuestionario),
    UNIQUE KEY uq_jugador_cuestionario_alias (id_cuestionario, alias),
    KEY indice_jugador (id_jugador),
    KEY indice_cuestionario (id_cuestionario),
    KEY indice_puntaje (puntaje DESC),
    CONSTRAINT Jugador_Cuestionario_ibfk_1 FOREIGN KEY (id_jugador) REFERENCES Jugador(id_jugador) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT Jugador_Cuestionario_ibfk_2 FOREIGN KEY (id_cuestionario) REFERENCES Cuestionario(id_cuestionario) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Paso 4: Recrear tabla Respuesta con referencia a Jugador_Cuestionario
CREATE TABLE IF NOT EXISTS Respuesta (
    id_respuesta INT AUTO_INCREMENT,
    id_jugador_cuestionario INT NOT NULL,
    id_pregunta INT NOT NULL,
    id_alternativa INT NOT NULL,
    tiempo_utilizado INT DEFAULT 0,
    fecha_respuesta DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_respuesta),
    UNIQUE KEY clave_unica_jugador_cuestionario_pregunta (id_jugador_cuestionario, id_pregunta),
    KEY indice_jugador_cuestionario (id_jugador_cuestionario),
    KEY indice_pregunta (id_pregunta),
    KEY indice_alternativa (id_alternativa),
    CONSTRAINT Respuesta_ibfk_1 FOREIGN KEY (id_jugador_cuestionario) REFERENCES Jugador_Cuestionario(id_jugador_cuestionario) ON DELETE CASCADE,
    CONSTRAINT Respuesta_ibfk_2 FOREIGN KEY (id_pregunta) REFERENCES Pregunta(id_pregunta) ON DELETE CASCADE,
    CONSTRAINT Respuesta_ibfk_3 FOREIGN KEY (id_alternativa) REFERENCES Alternativa(id_alternativa) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Paso 5: Recrear tabla Recompensa con referencia a Jugador_Cuestionario
CREATE TABLE IF NOT EXISTS Recompensa (
    id_recompensa INT AUTO_INCREMENT,
    id_cuestionario INT NOT NULL,
    id_jugador_cuestionario INT NOT NULL,
    id_jugador INT DEFAULT NULL,
    puntos INT NOT NULL DEFAULT 0,
    tipo_recompensa VARCHAR(50) DEFAULT 'puntos',
    fecha_recompensa DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_recompensa),
    UNIQUE KEY clave_unica_jugador_cuestionario_recompensa (id_cuestionario, id_jugador_cuestionario),
    KEY indice_cuestionario (id_cuestionario),
    KEY indice_jugador_cuestionario (id_jugador_cuestionario),
    KEY indice_jugador (id_jugador),
    CONSTRAINT Recompensa_ibfk_1 FOREIGN KEY (id_cuestionario) REFERENCES Cuestionario(id_cuestionario) ON DELETE CASCADE,
    CONSTRAINT Recompensa_ibfk_2 FOREIGN KEY (id_jugador_cuestionario) REFERENCES Jugador_Cuestionario(id_jugador_cuestionario) ON DELETE CASCADE,
    CONSTRAINT Recompensa_ibfk_3 FOREIGN KEY (id_jugador) REFERENCES Jugador(id_jugador) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Paso 6: Recrear tabla Grupo con referencia a Jugador_Cuestionario
CREATE TABLE IF NOT EXISTS Grupo (
    id_grupo INT AUTO_INCREMENT,
    nombre_grupo VARCHAR(100) NOT NULL,
    id_cuestionario INT NOT NULL,
    id_lider INT NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    metodo_evaluacion VARCHAR(20) DEFAULT 'votacion',
    estado VARCHAR(1) DEFAULT 'A',
    puntaje DECIMAL(10,2) DEFAULT 0.00,
    PRIMARY KEY (id_grupo),
    FOREIGN KEY (id_cuestionario) REFERENCES Cuestionario(id_cuestionario) ON DELETE CASCADE,
    FOREIGN KEY (id_lider) REFERENCES Jugador_Cuestionario(id_jugador_cuestionario) ON DELETE CASCADE,
    INDEX indice_cuestionario (id_cuestionario),
    INDEX indice_lider (id_lider)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Paso 7: Recrear tabla GrupoMiembro con referencia a Jugador_Cuestionario
CREATE TABLE IF NOT EXISTS GrupoMiembro (
    id_miembro INT AUTO_INCREMENT,
    id_grupo INT NOT NULL,
    id_jugador_cuestionario INT NOT NULL,
    fecha_union DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    es_lider TINYINT(1) DEFAULT 0,
    PRIMARY KEY (id_miembro),
    FOREIGN KEY (id_grupo) REFERENCES Grupo(id_grupo) ON DELETE CASCADE,
    FOREIGN KEY (id_jugador_cuestionario) REFERENCES Jugador_Cuestionario(id_jugador_cuestionario) ON DELETE CASCADE,
    UNIQUE KEY clave_unica_grupo_jugador_cuestionario (id_grupo, id_jugador_cuestionario),
    INDEX indice_grupo (id_grupo),
    INDEX indice_jugador_cuestionario (id_jugador_cuestionario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Paso 8: Recrear tabla RespuestaGrupo
CREATE TABLE IF NOT EXISTS RespuestaGrupo (
    id_respuesta_grupo INT AUTO_INCREMENT,
    id_grupo INT NOT NULL,
    id_pregunta INT NOT NULL,
    id_alternativa INT NOT NULL,
    tiempo_utilizado INT DEFAULT 0,
    fecha_respuesta DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_respuesta_grupo),
    FOREIGN KEY (id_grupo) REFERENCES Grupo(id_grupo) ON DELETE CASCADE,
    FOREIGN KEY (id_pregunta) REFERENCES Pregunta(id_pregunta) ON DELETE CASCADE,
    FOREIGN KEY (id_alternativa) REFERENCES Alternativa(id_alternativa) ON DELETE CASCADE,
    UNIQUE KEY clave_unica_grupo_pregunta (id_grupo, id_pregunta),
    INDEX indice_grupo (id_grupo),
    INDEX indice_pregunta (id_pregunta)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Paso 9: Recrear tabla VotacionGrupo con referencia a Jugador_Cuestionario
CREATE TABLE IF NOT EXISTS VotacionGrupo (
    id_votacion INT AUTO_INCREMENT,
    id_grupo INT NOT NULL,
    id_pregunta INT NOT NULL,
    id_jugador_cuestionario INT NOT NULL COMMENT 'Jugador que vota',
    id_alternativa INT NOT NULL COMMENT 'Alternativa por la que votó',
    fecha_votacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_votacion),
    UNIQUE KEY unique_grupo_pregunta_jugador_cuestionario (id_grupo, id_pregunta, id_jugador_cuestionario),
    KEY id_pregunta (id_pregunta),
    KEY id_alternativa (id_alternativa),
    KEY idx_grupo_pregunta (id_grupo, id_pregunta),
    KEY idx_jugador_cuestionario (id_jugador_cuestionario),
    CONSTRAINT VotacionGrupo_ibfk_1 FOREIGN KEY (id_grupo) REFERENCES Grupo(id_grupo) ON DELETE CASCADE,
    CONSTRAINT VotacionGrupo_ibfk_2 FOREIGN KEY (id_pregunta) REFERENCES Pregunta(id_pregunta) ON DELETE CASCADE,
    CONSTRAINT VotacionGrupo_ibfk_3 FOREIGN KEY (id_jugador_cuestionario) REFERENCES Jugador_Cuestionario(id_jugador_cuestionario) ON DELETE CASCADE,
    CONSTRAINT VotacionGrupo_ibfk_4 FOREIGN KEY (id_alternativa) REFERENCES Alternativa(id_alternativa) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- FIN DE LA MIGRACIÓN
-- ============================================
-- NOTA: Después de ejecutar este script, necesitarás actualizar
-- todo el código Python que hace referencia a:
-- - Usuario -> Jugador_Cuestionario
-- - id_usuario -> id_jugador_cuestionario
-- - Participante -> (eliminado)
-- - Participante_Cuestionario -> (eliminado)
-- ============================================

