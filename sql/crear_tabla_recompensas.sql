-- Tabla para almacenar las recompensas otorgadas a los jugadores
CREATE TABLE IF NOT EXISTS Recompensa (
    id_recompensa INT AUTO_INCREMENT PRIMARY KEY,
    id_cuestionario INT NOT NULL,
    id_usuario INT NOT NULL,
    id_jugador INT,
    puntos INT NOT NULL DEFAULT 0,
    tipo_recompensa VARCHAR(50) DEFAULT 'puntos',
    fecha_recompensa DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cuestionario) REFERENCES Cuestionario(id_cuestionario) ON DELETE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE,
    FOREIGN KEY (id_jugador) REFERENCES Jugador(id_jugador) ON DELETE SET NULL,
    UNIQUE KEY clave_unica_usuario_cuestionario (id_cuestionario, id_usuario),
    INDEX indice_cuestionario (id_cuestionario),
    INDEX indice_usuario (id_usuario),
    INDEX indice_jugador (id_jugador)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

