CREATE TABLE IF NOT EXISTS Grupo (
    id_grupo INT AUTO_INCREMENT PRIMARY KEY,
    nombre_grupo VARCHAR(100) NOT NULL,
    id_cuestionario INT NOT NULL,
    id_lider INT NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    metodo_evaluacion VARCHAR(20) DEFAULT 'votacion',
    estado VARCHAR(1) DEFAULT 'A',
    puntaje DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (id_cuestionario) REFERENCES Cuestionario(id_cuestionario) ON DELETE CASCADE,
    FOREIGN KEY (id_lider) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    INDEX indice_cuestionario (id_cuestionario),
    INDEX indice_lider (id_lider)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS GrupoMiembro (
    id_miembro INT AUTO_INCREMENT PRIMARY KEY,
    id_grupo INT NOT NULL,
    id_usuario INT NOT NULL,
    fecha_union DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    es_lider TINYINT(1) DEFAULT 0,
    FOREIGN KEY (id_grupo) REFERENCES Grupo(id_grupo) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    UNIQUE KEY clave_unica_grupo_usuario (id_grupo, id_usuario),
    INDEX indice_grupo (id_grupo),
    INDEX indice_usuario (id_usuario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS RespuestaGrupo (
    id_respuesta_grupo INT AUTO_INCREMENT PRIMARY KEY,
    id_grupo INT NOT NULL,
    id_pregunta INT NOT NULL,
    id_alternativa INT NOT NULL,
    tiempo_utilizado INT DEFAULT 0,
    fecha_respuesta DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_grupo) REFERENCES Grupo(id_grupo) ON DELETE CASCADE,
    FOREIGN KEY (id_pregunta) REFERENCES Pregunta(id_pregunta) ON DELETE CASCADE,
    FOREIGN KEY (id_alternativa) REFERENCES Alternativa(id_alternativa) ON DELETE CASCADE,
    UNIQUE KEY clave_unica_grupo_pregunta (id_grupo, id_pregunta),
    INDEX indice_grupo (id_grupo),
    INDEX indice_pregunta (id_pregunta)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS VotacionGrupo (
    id_votacion INT AUTO_INCREMENT PRIMARY KEY,
    id_grupo INT NOT NULL,
    id_pregunta INT NOT NULL,
    id_usuario INT NOT NULL,
    id_alternativa INT NOT NULL,
    fecha_votacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_grupo) REFERENCES Grupo(id_grupo) ON DELETE CASCADE,
    FOREIGN KEY (id_pregunta) REFERENCES Pregunta(id_pregunta) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_alternativa) REFERENCES Alternativa(id_alternativa) ON DELETE CASCADE,
    UNIQUE KEY clave_unica_grupo_pregunta_usuario (id_grupo, id_pregunta, id_usuario),
    INDEX indice_grupo_pregunta (id_grupo, id_pregunta),
    INDEX indice_usuario (id_usuario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

ALTER TABLE Alternativa 
MODIFY COLUMN respuesta TEXT NOT NULL;

ALTER TABLE Alternativa 
MODIFY COLUMN estado_alternativa TINYINT(1) NOT NULL DEFAULT 0;

CREATE INDEX IF NOT EXISTS indice_pregunta ON Alternativa(id_pregunta);
CREATE INDEX IF NOT EXISTS indice_estado_alternativa ON Alternativa(estado_alternativa);
