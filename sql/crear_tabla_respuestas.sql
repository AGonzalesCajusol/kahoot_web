-- Tabla para almacenar las respuestas individuales de los usuarios
CREATE TABLE IF NOT EXISTS Respuesta (
    id_respuesta INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_pregunta INT NOT NULL,
    id_alternativa INT NOT NULL,
    tiempo_utilizado INT DEFAULT 0,
    fecha_respuesta DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_pregunta) REFERENCES Pregunta(id_pregunta) ON DELETE CASCADE,
    FOREIGN KEY (id_alternativa) REFERENCES Alternativa(id_alternativa) ON DELETE CASCADE,
    UNIQUE KEY clave_unica_usuario_pregunta (id_usuario, id_pregunta),
    INDEX indice_usuario (id_usuario),
    INDEX indice_pregunta (id_pregunta),
    INDEX indice_alternativa (id_alternativa)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



























