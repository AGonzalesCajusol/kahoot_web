-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: preguntas-calculadoramateriales.e.aivencloud.com    Database: cuestionario
-- ------------------------------------------------------
-- Server version	8.0.35
-- Solo estructuras de tablas (sin datos)

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'cad7a24d-b47a-11f0-bfd4-bea84ea41ba0:1-507,
e04d9fd5-a0d7-11f0-98ae-9eac2fb876fb:1-286';

--
-- Table structure for table `Alternativa`
--

DROP TABLE IF EXISTS `Alternativa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Alternativa` (
  `id_alternativa` int NOT NULL AUTO_INCREMENT,
  `respuesta` varchar(255) NOT NULL,
  `estado_alternativa` tinyint(1) DEFAULT NULL,
  `id_pregunta` int NOT NULL,
  PRIMARY KEY (`id_alternativa`),
  KEY `Alternativa_ibfk_1` (`id_pregunta`),
  CONSTRAINT `Alternativa_ibfk_1` FOREIGN KEY (`id_pregunta`) REFERENCES `Pregunta` (`id_pregunta`)
) ENGINE=InnoDB AUTO_INCREMENT=275 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Cuestionario`
--

DROP TABLE IF EXISTS `Cuestionario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Cuestionario` (
  `id_cuestionario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `estado` char(1) NOT NULL,
  `id_docente` int NOT NULL,
  `tipo_cuestionario` char(1) NOT NULL,
  `pin` char(5) NOT NULL,
  `descripcion` text,
  `estado_cuestionario` char(1) NOT NULL DEFAULT 'A',
  `estado_juego` char(2) NOT NULL DEFAULT 'SL',
  `imagen_url` varchar(255) DEFAULT NULL COMMENT 'Ruta de la imagen del cuestionario (opcional)',
  PRIMARY KEY (`id_cuestionario`),
  UNIQUE KEY `pin_UNIQUE` (`pin`),
  KEY `Cuestionario_ibfk_1` (`id_docente`),
  KEY `idx_pin_estado` (`pin`,`estado_cuestionario`),
  CONSTRAINT `Cuestionario_ibfk_1` FOREIGN KEY (`id_docente`) REFERENCES `Docente` (`id_docente`),
  CONSTRAINT `Cuestionario_chk_1` CHECK ((`estado_cuestionario` in (_utf8mb4'A',_utf8mb4'I'))),
  CONSTRAINT `Cuestionario_chk_2` CHECK ((`estado_juego` in (_utf8mb4'SL',_utf8mb4'IN',_utf8mb4'FN')))
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Docente`
--

DROP TABLE IF EXISTS `Docente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Docente` (
  `id_docente` int NOT NULL AUTO_INCREMENT,
  `correo` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nombres` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `token` varchar(255) DEFAULT NULL,
  `rostro` text,
  PRIMARY KEY (`id_docente`),
  UNIQUE KEY `correo_UNIQUE` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Grupo`
--

DROP TABLE IF EXISTS `Grupo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Grupo` (
  `id_grupo` int NOT NULL AUTO_INCREMENT,
  `nombre_grupo` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_cuestionario` int NOT NULL,
  `id_lider` int NOT NULL,
  `fecha_creacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `metodo_evaluacion` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'votacion',
  `estado` varchar(1) COLLATE utf8mb4_unicode_ci DEFAULT 'A',
  `puntaje` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`id_grupo`),
  KEY `indice_cuestionario` (`id_cuestionario`),
  KEY `indice_lider` (`id_lider`),
  CONSTRAINT `Grupo_ibfk_1` FOREIGN KEY (`id_cuestionario`) REFERENCES `Cuestionario` (`id_cuestionario`) ON DELETE CASCADE,
  CONSTRAINT `Grupo_ibfk_2` FOREIGN KEY (`id_lider`) REFERENCES `Jugador_Cuestionario` (`id_jugador_cuestionario`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `GrupoMiembro`
--

DROP TABLE IF EXISTS `GrupoMiembro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `GrupoMiembro` (
  `id_miembro` int NOT NULL AUTO_INCREMENT,
  `id_grupo` int NOT NULL,
  `id_jugador_cuestionario` int NOT NULL,
  `fecha_union` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `es_lider` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id_miembro`),
  UNIQUE KEY `clave_unica_grupo_jugador_cuestionario` (`id_grupo`,`id_jugador_cuestionario`),
  KEY `indice_grupo` (`id_grupo`),
  KEY `indice_jugador_cuestionario` (`id_jugador_cuestionario`),
  CONSTRAINT `GrupoMiembro_ibfk_1` FOREIGN KEY (`id_grupo`) REFERENCES `Grupo` (`id_grupo`) ON DELETE CASCADE,
  CONSTRAINT `GrupoMiembro_ibfk_2` FOREIGN KEY (`id_jugador_cuestionario`) REFERENCES `Jugador_Cuestionario` (`id_jugador_cuestionario`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Jugador`
--

DROP TABLE IF EXISTS `Jugador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Jugador` (
  `id_jugador` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) DEFAULT NULL,
  `contraseña` varchar(255) NOT NULL,
  `rostro` text,
  PRIMARY KEY (`id_jugador`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Jugador_Cuestionario`
--

DROP TABLE IF EXISTS `Jugador_Cuestionario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Jugador_Cuestionario` (
  `id_jugador_cuestionario` int NOT NULL AUTO_INCREMENT,
  `id_jugador` int NOT NULL,
  `id_cuestionario` int NOT NULL,
  `alias` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `puntaje` decimal(5,2) NOT NULL DEFAULT '0.00',
  `fecha_participacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_jugador_cuestionario`),
  UNIQUE KEY `uq_jugador_cuestionario_alias` (`id_cuestionario`,`alias`),
  UNIQUE KEY `uq_jugador_cuestionario` (`id_jugador`,`id_cuestionario`),
  KEY `indice_jugador` (`id_jugador`),
  KEY `indice_cuestionario` (`id_cuestionario`),
  KEY `indice_puntaje` (`puntaje` DESC),
  CONSTRAINT `Jugador_Cuestionario_ibfk_1` FOREIGN KEY (`id_jugador`) REFERENCES `Jugador` (`id_jugador`) ON DELETE CASCADE,
  CONSTRAINT `Jugador_Cuestionario_ibfk_2` FOREIGN KEY (`id_cuestionario`) REFERENCES `Cuestionario` (`id_cuestionario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Pregunta`
--

DROP TABLE IF EXISTS `Pregunta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Pregunta` (
  `id_pregunta` int NOT NULL AUTO_INCREMENT,
  `pregunta` varchar(255) NOT NULL,
  `puntaje` int NOT NULL,
  `tiempo_respuesta` int NOT NULL,
  `tipo_pregunta` char(3) NOT NULL,
  `id_cuestionario` int NOT NULL,
  PRIMARY KEY (`id_pregunta`),
  KEY `Pregunta_ibfk_1` (`id_cuestionario`),
  CONSTRAINT `Pregunta_ibfk_1` FOREIGN KEY (`id_cuestionario`) REFERENCES `Cuestionario` (`id_cuestionario`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Recompensa`
--

DROP TABLE IF EXISTS `Recompensa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Recompensa` (
  `id_recompensa` int NOT NULL AUTO_INCREMENT,
  `id_cuestionario` int NOT NULL,
  `id_jugador_cuestionario` int NOT NULL,
  `id_jugador` int DEFAULT NULL,
  `puntos` int NOT NULL DEFAULT '0',
  `tipo_recompensa` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT 'puntos',
  `fecha_recompensa` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_recompensa`),
  UNIQUE KEY `clave_unica_jugador_cuestionario_recompensa` (`id_cuestionario`,`id_jugador_cuestionario`),
  KEY `indice_cuestionario` (`id_cuestionario`),
  KEY `indice_jugador_cuestionario` (`id_jugador_cuestionario`),
  KEY `indice_jugador` (`id_jugador`),
  CONSTRAINT `Recompensa_ibfk_1` FOREIGN KEY (`id_cuestionario`) REFERENCES `Cuestionario` (`id_cuestionario`) ON DELETE CASCADE,
  CONSTRAINT `Recompensa_ibfk_2` FOREIGN KEY (`id_jugador_cuestionario`) REFERENCES `Jugador_Cuestionario` (`id_jugador_cuestionario`) ON DELETE CASCADE,
  CONSTRAINT `Recompensa_ibfk_3` FOREIGN KEY (`id_jugador`) REFERENCES `Jugador` (`id_jugador`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Respuesta`
--

DROP TABLE IF EXISTS `Respuesta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Respuesta` (
  `id_respuesta` int NOT NULL AUTO_INCREMENT,
  `id_jugador_cuestionario` int NOT NULL,
  `id_pregunta` int NOT NULL,
  `id_alternativa` int NOT NULL,
  `tiempo_utilizado` int DEFAULT '0',
  `fecha_respuesta` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_respuesta`),
  UNIQUE KEY `clave_unica_jugador_cuestionario_pregunta` (`id_jugador_cuestionario`,`id_pregunta`),
  KEY `indice_jugador_cuestionario` (`id_jugador_cuestionario`),
  KEY `indice_pregunta` (`id_pregunta`),
  KEY `indice_alternativa` (`id_alternativa`),
  CONSTRAINT `Respuesta_ibfk_1` FOREIGN KEY (`id_jugador_cuestionario`) REFERENCES `Jugador_Cuestionario` (`id_jugador_cuestionario`) ON DELETE CASCADE,
  CONSTRAINT `Respuesta_ibfk_2` FOREIGN KEY (`id_pregunta`) REFERENCES `Pregunta` (`id_pregunta`) ON DELETE CASCADE,
  CONSTRAINT `Respuesta_ibfk_3` FOREIGN KEY (`id_alternativa`) REFERENCES `Alternativa` (`id_alternativa`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `RespuestaGrupo`
--

DROP TABLE IF EXISTS `RespuestaGrupo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RespuestaGrupo` (
  `id_respuesta_grupo` int NOT NULL AUTO_INCREMENT,
  `id_grupo` int NOT NULL,
  `id_pregunta` int NOT NULL,
  `id_alternativa` int NOT NULL,
  `tiempo_utilizado` int DEFAULT '0',
  `fecha_respuesta` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_respuesta_grupo`),
  UNIQUE KEY `clave_unica_grupo_pregunta` (`id_grupo`,`id_pregunta`),
  KEY `id_alternativa` (`id_alternativa`),
  KEY `indice_grupo` (`id_grupo`),
  KEY `indice_pregunta` (`id_pregunta`),
  CONSTRAINT `RespuestaGrupo_ibfk_1` FOREIGN KEY (`id_grupo`) REFERENCES `Grupo` (`id_grupo`) ON DELETE CASCADE,
  CONSTRAINT `RespuestaGrupo_ibfk_2` FOREIGN KEY (`id_pregunta`) REFERENCES `Pregunta` (`id_pregunta`) ON DELETE CASCADE,
  CONSTRAINT `RespuestaGrupo_ibfk_3` FOREIGN KEY (`id_alternativa`) REFERENCES `Alternativa` (`id_alternativa`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `VotacionGrupo`
--

DROP TABLE IF EXISTS `VotacionGrupo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `VotacionGrupo` (
  `id_votacion` int NOT NULL AUTO_INCREMENT,
  `id_grupo` int NOT NULL,
  `id_pregunta` int NOT NULL,
  `id_jugador_cuestionario` int NOT NULL COMMENT 'Jugador que vota',
  `id_alternativa` int NOT NULL COMMENT 'Alternativa por la que votó',
  `fecha_votacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_votacion`),
  UNIQUE KEY `unique_grupo_pregunta_jugador_cuestionario` (`id_grupo`,`id_pregunta`,`id_jugador_cuestionario`),
  KEY `id_pregunta` (`id_pregunta`),
  KEY `id_alternativa` (`id_alternativa`),
  KEY `idx_grupo_pregunta` (`id_grupo`,`id_pregunta`),
  KEY `idx_jugador_cuestionario` (`id_jugador_cuestionario`),
  CONSTRAINT `VotacionGrupo_ibfk_1` FOREIGN KEY (`id_grupo`) REFERENCES `Grupo` (`id_grupo`) ON DELETE CASCADE,
  CONSTRAINT `VotacionGrupo_ibfk_2` FOREIGN KEY (`id_pregunta`) REFERENCES `Pregunta` (`id_pregunta`) ON DELETE CASCADE,
  CONSTRAINT `VotacionGrupo_ibfk_3` FOREIGN KEY (`id_jugador_cuestionario`) REFERENCES `Jugador_Cuestionario` (`id_jugador_cuestionario`) ON DELETE CASCADE,
  CONSTRAINT `VotacionGrupo_ibfk_4` FOREIGN KEY (`id_alternativa`) REFERENCES `Alternativa` (`id_alternativa`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-01  2:17:22
-- Solo estructuras de tablas (sin datos)










