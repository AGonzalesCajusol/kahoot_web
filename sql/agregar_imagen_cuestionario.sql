-- Agregar campo imagen_url a la tabla Cuestionario
ALTER TABLE Cuestionario 
ADD COLUMN imagen_url VARCHAR(255) NULL DEFAULT NULL 
COMMENT 'Ruta de la imagen del cuestionario (opcional)';










