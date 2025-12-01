-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: preguntas-calculadoramateriales.e.aivencloud.com    Database: cuestionario
-- ------------------------------------------------------
-- Server version	8.0.35

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

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'cad7a24d-b47a-11f0-bfd4-bea84ea41ba0:1-317,
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
) ENGINE=InnoDB AUTO_INCREMENT=215 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Alternativa`
--

LOCK TABLES `Alternativa` WRITE;
/*!40000 ALTER TABLE `Alternativa` DISABLE KEYS */;
INSERT INTO `Alternativa` VALUES (1,'V',1,2),(2,'F',0,2),(3,'X',1,2),(4,'Domingo ',0,5),(5,'Lunes',0,5),(6,'Martes',0,5),(7,'Domingo ',0,6),(8,'Lunes',0,6),(9,'Martes',0,6),(10,'2',1,7),(11,'1',0,7),(12,'3',0,7),(13,'V',1,8),(14,'F',0,8),(30,'X',0,13),(31,',',0,13),(32,'Y',1,13),(33,',',0,13),(34,'Z',0,13),(40,'X',0,15),(41,',',0,15),(42,'Y',1,15),(43,',',0,15),(44,'Z',0,15),(45,'1',0,16),(46,',',0,16),(47,'2',0,16),(48,',',0,16),(49,'3',0,16),(50,'1',0,17),(51,',',0,17),(52,'2',0,17),(53,',',0,17),(54,'3',0,17),(55,'1',0,18),(56,',',0,18),(57,'2',0,18),(58,',',0,18),(59,'3',0,18),(60,'1',0,19),(61,',',0,19),(62,'2',0,19),(63,',',0,19),(64,'3',0,19),(65,'1',0,20),(66,',',0,20),(67,'2',0,20),(68,',',0,20),(69,'3',0,20),(70,'1',0,21),(71,',',0,21),(72,'2',0,21),(73,',',0,21),(74,'3',0,21),(75,'1',0,22),(76,',',0,22),(77,'2',0,22),(78,',',0,22),(79,'3',0,22),(80,'1',0,23),(81,',',0,23),(82,'2',0,23),(83,',',0,23),(84,'3',0,23),(85,'1',0,24),(86,',',0,24),(87,'2',0,24),(88,',',0,24),(89,'3',0,24),(90,'Verdadero',1,25),(91,'Falso',0,25),(104,'1',0,30),(105,',',0,30),(106,'2',0,30),(107,',',0,30),(108,'3',0,30),(109,'1',0,31),(110,',',0,31),(111,'2',0,31),(112,',',0,31),(113,'3',0,31),(134,'1',0,36),(135,',',0,36),(136,'2',0,36),(137,',',0,36),(138,'3',0,36),(139,'1',0,37),(140,',',0,37),(141,'2',0,37),(142,',',0,37),(143,'3',0,37),(144,'1',0,38),(145,' ',0,38),(146,'2',0,38),(147,' ',0,38),(148,'3',0,38),(149,'1',0,39),(150,' ',0,39),(151,'2',0,39),(152,' ',0,39),(153,'3',0,39),(154,'1',0,40),(155,' ',0,40),(156,'2',0,40),(157,' ',0,40),(158,'3',0,40),(159,'1',0,41),(160,' ',0,41),(161,'2',0,41),(162,' ',0,41),(163,'3',0,41),(164,'1',0,42),(165,' ',0,42),(166,'2',0,42),(167,' ',0,42),(168,'3',0,42),(169,'1',0,43),(170,' ',0,43),(171,'2',0,43),(172,' ',0,43),(173,'3',0,43),(174,'ALT',0,44),(175,'ALT',0,45),(176,'ALT',0,46),(177,'ALT',0,47),(178,'ALT',0,48),(179,'ALT',0,49),(180,'ALT',0,50),(181,'ALT',0,51),(182,'ALT',0,52),(183,'ALT',0,53),(184,'1 2 3',0,54),(185,'1 2 3',0,55),(186,'2',0,56),(187,'3',1,56),(188,'4',0,56),(189,'5',0,57),(190,'4',1,57),(191,'3',0,57),(192,'1',0,58),(193,'2',0,58),(194,'6',1,58),(195,'3',0,58),(196,'4',1,59),(197,'5',0,59),(198,'2',0,59),(199,'3',0,59),(200,'12',0,60),(201,'14',0,60),(202,'23',1,60),(203,'2',1,61),(204,'3',0,61),(205,'5',0,61),(209,'1',0,34),(210,'2',1,34),(211,'3',0,34),(212,'1',1,35),(213,'2',0,35),(214,'3',0,35);
/*!40000 ALTER TABLE `Alternativa` ENABLE KEYS */;
UNLOCK TABLES;

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
  PRIMARY KEY (`id_cuestionario`),
  UNIQUE KEY `pin_UNIQUE` (`pin`),
  KEY `Cuestionario_ibfk_1` (`id_docente`),
  KEY `idx_pin_estado` (`pin`,`estado_cuestionario`),
  CONSTRAINT `Cuestionario_ibfk_1` FOREIGN KEY (`id_docente`) REFERENCES `Docente` (`id_docente`),
  CONSTRAINT `Cuestionario_chk_1` CHECK ((`estado_cuestionario` in (_utf8mb4'A',_utf8mb4'I'))),
  CONSTRAINT `Cuestionario_chk_2` CHECK ((`estado_juego` in (_utf8mb4'SL',_utf8mb4'IN',_utf8mb4'FN')))
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cuestionario`
--

LOCK TABLES `Cuestionario` WRITE;
/*!40000 ALTER TABLE `Cuestionario` DISABLE KEYS */;
INSERT INTO `Cuestionario` VALUES (1,'Cuestionario de Matemáticas','P',29,'I','12345','Cuestionario de matemáticas para alumnos de secundaria.','A','FN'),(2,'Cuestionario de Historia','R',29,'I','54321','Cuestionario sobre historia del Perú para estudiantes de primaria.','A','FN'),(3,'Cuestionario de Física','R',29,'G','67890','Cuestionario sobre conceptos básicos de física para estudiantes universitarios.','A','FN'),(4,'Cuestionario de Lengua Española','P',29,'G','23135','Cuestionario para evaluar la ortografía y gramática en lengua española.','A','SL'),(5,'Cuestionario de Química','P',29,'I','44556','Cuestionario sobre reacciones químicas y átomos para nivel medio.','A','SL'),(6,'Cuestionario de Matemáticas','P',29,'I','64612','Cuestionario de matemáticas para secundaria','A','FN'),(7,'Cuestionario de Historia','P',29,'I','ABCDE','Cuestionario sobre historia mundial para estudiantes de secundaria.','I','SL'),(10,'','',29,'','12312','','I','SL'),(11,'Hola como estas?','P',29,'I','23413','zdfghjk-','A','FN'),(12,'Hola como estas?','P',29,'I','56465','zdfghjk-','A','FN'),(21,'Cuestionario general','P',29,'G','33924','Prueba lógica','A','SL'),(22,'Cuestionario general','P',29,'G','76186','Prueba lógica','A','FN'),(25,'Cuestionario xxx','P',29,'G','39383','Descripcion general del formulario xxxx','A','SL'),(26,'Cuestionario xxx','P',29,'G','50383','Descripcion general del formulario xxxx','A','FN'),(27,'Cuestionario xxx','P',29,'G','42465','Descripcion general del formulario xxxx','A','SL'),(28,'Cuestionario xxx','P',29,'G','33382','Descripcion general del formulario xxxx','A','FN'),(29,'Arroz con pato','P',29,'I','18596','yyy','A','FN'),(41,'TEMPORALES6','P',46,'G','61844','PROBANDO','A','SL'),(43,'TEMPORALE26','P',46,'I','68359','PROBANDO','A','FN'),(44,'TEMPORAL4','P',46,'I','26799','PROBANDO','A','FN'),(45,'TEMPORAL5','P',46,'I','91916','PROBANDO','A','FN'),(46,'TEMPORAL6','P',46,'I','82367','PROBANDO','A','FN'),(47,'TEMPORAL7','P',46,'I','69082','PROBANDO','A','FN'),(48,'TEMPORAL8','P',46,'P','78439','Individual','A','FN'),(49,'TEMPORAL9','P',46,'P','98853','Individual','A','IN'),(50,'TEMPORAL10','P',46,'P','35088','Individual','A','FN'),(51,'TEMPORAL11','P',46,'P','42780','Individual','A','FN'),(52,'TEMPORAL12','P',46,'P','76239','Individual','A','FN'),(53,'TEMPORAL13','P',46,'P','31975','Individual','A','SL'),(54,'qwe','P',46,'I','31148','qwe','A','SL'),(55,'Jesus123','P',46,'I','34677','1231','A','SL'),(56,'chuisito','P',46,'I','17185','qwewqe','A','FN'),(57,'jesus','R',46,'I','77349','123','A','FN');
/*!40000 ALTER TABLE `Cuestionario` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `Docente`
--

LOCK TABLES `Docente` WRITE;
/*!40000 ALTER TABLE `Docente` DISABLE KEYS */;
INSERT INTO `Docente` VALUES (1,'kahootbamba@gmail.com','hola1234','Carlitos','Carlitos',NULL,NULL),(29,'anggelo243120@gmail.com','55e24ca28a887c3e8898eb2cc92bd26f8e2576832e9805e16f9ba5e60be7486d','jooo2','waaa1',NULL,NULL),(31,'chui@gmail.com','ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f','jesus','chapoñan',NULL,NULL),(33,'qwertyu23058@gmail.com','ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f','test','劉',NULL,NULL),(34,'pruebaaaa@gmail.com','c775e7b757ede630cd0aa1113bd102661ab38829ca52a6422ab782862f268646','prueba','prieba',NULL,NULL),(35,'prueba23@gmail.com','3871490800b8c864d7cc1434b47361026082abb4d130945f16f350494b54128b','prueba','prieba',NULL,NULL),(36,'p@gmail.com','c60366f471b341631a142aa5523b079743961ed3a36116d82f2072132d0e915e','prueba','prieba',NULL,NULL),(37,'grupo01chat@gmail.com','6325af9d9e3e0e66944564f30ef67b3390610b00d2ec645bacb02ff39763797b','chui','chapo',NULL,NULL),(46,'mixdjangel7@gmail.com','b2ab0ab5438c6ea60625516e95dc976afe7daf9beccf7c06cf2a3ddbed237420','jesus','paico paico',NULL,'[0.0, 2.6099390942838267e-10, 1.0961744195992072e-08, 5.6838673608847776e-09, 4.262900520663583e-09, 6.089857886662262e-09, 4.610892399901427e-09, 5.5388707445356765e-09, 5.567870067805497e-09, 2.92893165025185e-09, 3.044928943331131e-09, 3.711913378536998e-09, 2.754935710632928e-09, 3.6829140552671773e-09, 5.074881572218551e-09, 4.523894430091966e-09, 5.480872097996036e-09, 6.147856533201903e-09, 5.741866007424419e-09, 6.3798511193604646e-09, 6.727842998598309e-09, 6.84384029167759e-09, 5.335875481646934e-09, 6.3798511193604646e-09, 5.567870067805497e-09, 7.365828110534355e-09, 7.307829463994714e-09, 8.496801718057346e-09, 8.90279224383483e-09, 9.134786829993392e-09, 9.337782092882135e-09, 1.0410757053865485e-08, 1.0787748256373149e-08, 1.1657727954467759e-08, 1.670361020341649e-08, 1.9168552681351216e-08, 1.8240574336716965e-08, 1.7631588548050738e-08, 1.6964604112844872e-08, 1.879156147884355e-08, 2.2242480947952167e-08, 2.1430499896397198e-08, 2.2648471473729652e-08, 1.9429546590779597e-08, 1.7051602082654334e-08, 1.0961744195992072e-08, 1.0845746902912791e-08, 8.554800364596988e-09, 6.611845705519027e-09, 6.611845705519027e-09, 3.624915408727537e-09, 2.6099390942838266e-09, 3.1029275898707716e-09, 2.5229411244743655e-09, 1.5949627798401161e-09, 6.089857886662262e-10, 2.3199458615856237e-10, 2.8999323269820296e-11, 8.699796980946089e-11, 2.8999323269820296e-11, 2.8999323269820296e-11, 5.799864653964059e-11, 0.0, 0.0, 0.9999830499915491, 2.7765862935889635e-05, 3.0851464993736115e-05, 0.0005961740369781254, -8.741824661439054e-05, 0.0005571663001491298, 0.0053543122908909745, -0.0020376391432122627, -1.3602170442129895e-05, -0.0006173588799991124, 9.468279047596327e-08, 1.170122693937249e-07, 8.238707740955946e-08, 5.153179745047066e-08, 3.6829140552671776e-08, 2.435943154664905e-08, 1.6906605466305233e-08, 1.2150716450054704e-08, 9.192785476533034e-09, 6.089857886662262e-09, 4.6978903697108875e-09, 3.5669167621878964e-09, 2.435943154664905e-09, 2.435943154664905e-09, 1.6819607496495772e-09, 1.6239621031099366e-09, 1.4209668402211944e-09, 1.2469709006022726e-09, 1.1019742842531711e-09, 9.569776679040698e-10, 4.92988495586945e-10, 3.769912025076638e-10, 4.92988495586945e-10, 4.6398917231712474e-10, 1.4499661634910147e-10, 2.0299526288874207e-10, 1.7399593961892177e-10, 2.6099390942838267e-10, 8.699796980946089e-11, 5.799864653964059e-11, 0.0, 5.799864653964059e-11, 1.473165622106871e-08, 0.0, 8.148809838819503e-09, 1.4586659604719609e-08, 0.0, 0.0, 1.2875699531800212e-08, 5.614268985037209e-08, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 5.2488775118374734e-09, 1.884956012538319e-09, 0.0, 0.0, 3.088427928235861e-08, 1.8182575690177326e-08, 6.103412170358576e-05, 2.4646734925493615e-05, 6.746773756828848e-05, 3.32587438716915e-06, 0.00011688072846337299]');
/*!40000 ALTER TABLE `Docente` ENABLE KEYS */;
UNLOCK TABLES;

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
  `id_lider` int NOT NULL COMMENT 'Usuario que creó el grupo',
  `fecha_creacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `metodo_evaluacion` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'votacion' COMMENT 'votacion: mayoría, consenso: unanimidad, lider: decide líder',
  `estado` varchar(1) COLLATE utf8mb4_unicode_ci DEFAULT 'A' COMMENT 'A: Activo, D: Disuelto',
  `puntaje` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`id_grupo`),
  KEY `idx_cuestionario` (`id_cuestionario`),
  KEY `idx_lider` (`id_lider`),
  CONSTRAINT `Grupo_ibfk_1` FOREIGN KEY (`id_cuestionario`) REFERENCES `Cuestionario` (`id_cuestionario`) ON DELETE CASCADE,
  CONSTRAINT `Grupo_ibfk_2` FOREIGN KEY (`id_lider`) REFERENCES `Usuario` (`id_usuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Grupo`
--

LOCK TABLES `Grupo` WRITE;
/*!40000 ALTER TABLE `Grupo` DISABLE KEYS */;
/*!40000 ALTER TABLE `Grupo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `GrupoMiembro`
--

DROP TABLE IF EXISTS `GrupoMiembro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `GrupoMiembro` (
  `id_miembro` int NOT NULL AUTO_INCREMENT,
  `id_grupo` int NOT NULL,
  `id_usuario` int NOT NULL,
  `fecha_union` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `es_lider` tinyint(1) DEFAULT '0' COMMENT '1: Es líder, 0: No es líder',
  PRIMARY KEY (`id_miembro`),
  UNIQUE KEY `unique_grupo_usuario` (`id_grupo`,`id_usuario`),
  KEY `idx_grupo` (`id_grupo`),
  KEY `idx_usuario` (`id_usuario`),
  CONSTRAINT `GrupoMiembro_ibfk_1` FOREIGN KEY (`id_grupo`) REFERENCES `Grupo` (`id_grupo`) ON DELETE CASCADE,
  CONSTRAINT `GrupoMiembro_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `Usuario` (`id_usuario`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `GrupoMiembro`
--

LOCK TABLES `GrupoMiembro` WRITE;
/*!40000 ALTER TABLE `GrupoMiembro` DISABLE KEYS */;
/*!40000 ALTER TABLE `GrupoMiembro` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Dumping data for table `Jugador`
--

LOCK TABLES `Jugador` WRITE;
/*!40000 ALTER TABLE `Jugador` DISABLE KEYS */;
INSERT INTO `Jugador` VALUES (1,'andres.sanchez@example.com','',NULL),(2,'carlos.perez@example.com','',NULL),(3,'ana.torres@example.com','',NULL),(4,'maria.gomez@example.com','',NULL),(5,'juan.lopez@example.com','',NULL),(6,'luis.martinez@example.com','',NULL),(7,'sofia.ramirez@example.com','',NULL),(8,'diego.fernandez@example.com','',NULL),(9,'valentina.rodriguez@example.com','',NULL),(10,'camila.morales@example.com','',NULL),(11,'uxux393@gmail.com','55e24ca28a887c3e8898eb2cc92bd26f8e2576832e9805e16f9ba5e60be7486d',NULL),(12,'uxux89322@gmail.com','55e24ca28a887c3e8898eb2cc92bd26f8e2576832e9805e16f9ba5e60be7486d',NULL),(17,'62774214@usat.pe','b2ab0ab5438c6ea60625516e95dc976afe7daf9beccf7c06cf2a3ddbed237420',NULL);
/*!40000 ALTER TABLE `Jugador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Participante`
--

DROP TABLE IF EXISTS `Participante`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Participante` (
  `id_participante` varchar(80) NOT NULL,
  PRIMARY KEY (`id_participante`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Participante`
--

LOCK TABLES `Participante` WRITE;
/*!40000 ALTER TABLE `Participante` DISABLE KEYS */;
INSERT INTO `Participante` VALUES ('c23ce6c6-5e56-428c-91b7-e9c6b4be2134'),('e41e95cc-3c3a-4095-9986-971af515a776');
/*!40000 ALTER TABLE `Participante` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Participante_Cuestionario`
--

DROP TABLE IF EXISTS `Participante_Cuestionario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Participante_Cuestionario` (
  `id_participante` varchar(80) NOT NULL,
  `id_cuestionario` int NOT NULL,
  `alias` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_participante`,`id_cuestionario`),
  CONSTRAINT `Participante_Cuestionario_ibfk_1` FOREIGN KEY (`id_participante`) REFERENCES `Participante` (`id_participante`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Participante_Cuestionario`
--

LOCK TABLES `Participante_Cuestionario` WRITE;
/*!40000 ALTER TABLE `Participante_Cuestionario` DISABLE KEYS */;
/*!40000 ALTER TABLE `Participante_Cuestionario` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pregunta`
--

LOCK TABLES `Pregunta` WRITE;
/*!40000 ALTER TABLE `Pregunta` DISABLE KEYS */;
INSERT INTO `Pregunta` VALUES (1,'¿Cuánto es 2 + 2?',10,30,'V',6),(2,'¿Quién fue el primer presidente de Estados Unidos?',10,30,'V',6),(3,'¿En qué año se firmó la independencia de Estados Unidos?',10,30,'V',6),(5,'¿Que día es hoy?',5,12,'ALT',10),(6,'¿Que día es hoy?',5,12,'ALT',11),(7,'¿Cuánto es 1 +1?',5,12,'ALT',12),(8,'¿cuanto es 2 +2?',5,12,'V',12),(13,'¿Por qué hoy es jueves?',5,5,'V',21),(14,'¿Cuánto es 1+1?',8,4,'ALT',21),(15,'¿Por qué hoy es jueves?',5,5,'V',22),(16,'¿Cuánto es 1+1?',8,4,'ALT',22),(17,'Pregunta xxx',8,4,'V',25),(18,'Pregunta yyy',8,4,'ALT',25),(19,'Pregunta xxx',8,4,'V',26),(20,'Pregunta yyy',8,4,'ALT',26),(21,'Pregunta xxx',8,4,'V',27),(22,'Pregunta yyy',8,4,'ALT',27),(23,'Pregunta xxx',8,4,'V',28),(24,'Pregunta yyy',8,4,'ALT',28),(25,'asdasd',12,12,'VF',29),(30,'CUANDO ES 1+1?',10,4,'ALT',41),(31,'CUANDO ES 0+1?',8,4,'ALT',41),(34,'CUANDO ES 1+1?',10,10,'ALT',43),(35,'CUANDO ES 0+1?',8,10,'ALT',43),(36,'CUANDO ES 1+1?',10,4,'ALT',44),(37,'CUANDO ES 0+1?',8,4,'ALT',44),(38,'CUANDO ES 1+1?',10,4,'ALT',45),(39,'CUANDO ES 0+1?',8,4,'ALT',45),(40,'CUANDO ES 1+1?',10,4,'ALT',46),(41,'CUANDO ES 0+1?',8,4,'ALT',46),(42,'CUANDO ES 1+1?',10,4,'ALT',47),(43,'CUANDO ES 0+1?',8,4,'ALT',47),(44,'CUANDO ES 1+1?',2,10,'ALT',48),(45,'CUANDO ES 0+1?',1,8,'ALT',48),(46,'CUANDO ES 1+1?',2,10,'ALT',49),(47,'CUANDO ES 0+1?',1,8,'ALT',49),(48,'CUANDO ES 1+1?',2,10,'ALT',50),(49,'CUANDO ES 0+1?',1,8,'ALT',50),(50,'CUANDO ES 1+1?',2,10,'ALT',51),(51,'CUANDO ES 0+1?',1,8,'ALT',51),(52,'CUANDO ES 1+1?',2,10,'ALT',52),(53,'CUANDO ES 0+1?',1,8,'ALT',52),(54,'CUANDO ES 1+1?',10,4,'ALT',53),(55,'CUANDO ES 0+1?',8,4,'ALT',53),(56,'Cuanto es 1+2?',12,12,'ALT',54),(57,'CUANTO ES 2+2?',12,12,'ALT',55),(58,'Cuanto es 1+5?',12,12,'ALT',56),(59,'cuanto es 7-3?',12,12,'ALT',56),(60,'Cuantos años tengo?',12,12,'ALT',57),(61,'Cuanto es 1+1?',12,12,'ALT',57);
/*!40000 ALTER TABLE `Pregunta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Recompensa`
--

DROP TABLE IF EXISTS `Recompensa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Recompensa` (
  `id_recompensa` int NOT NULL AUTO_INCREMENT,
  `id_cuestionario` int NOT NULL,
  `id_usuario` int NOT NULL,
  `id_jugador` int DEFAULT NULL,
  `puntos` int NOT NULL DEFAULT '0',
  `tipo_recompensa` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT 'puntos',
  `fecha_recompensa` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_recompensa`),
  UNIQUE KEY `clave_unica_usuario_cuestionario` (`id_cuestionario`,`id_usuario`),
  KEY `indice_cuestionario` (`id_cuestionario`),
  KEY `indice_usuario` (`id_usuario`),
  KEY `indice_jugador` (`id_jugador`),
  CONSTRAINT `Recompensa_ibfk_1` FOREIGN KEY (`id_cuestionario`) REFERENCES `Cuestionario` (`id_cuestionario`) ON DELETE CASCADE,
  CONSTRAINT `Recompensa_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `Usuario` (`id_usuario`) ON DELETE CASCADE,
  CONSTRAINT `Recompensa_ibfk_3` FOREIGN KEY (`id_jugador`) REFERENCES `Jugador` (`id_jugador`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Recompensa`
--

LOCK TABLES `Recompensa` WRITE;
/*!40000 ALTER TABLE `Recompensa` DISABLE KEYS */;
INSERT INTO `Recompensa` VALUES (1,56,99,NULL,100,'puntos','2025-11-11 15:32:16');
/*!40000 ALTER TABLE `Recompensa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Respuesta`
--

DROP TABLE IF EXISTS `Respuesta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Respuesta` (
  `id_respuesta` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `id_pregunta` int NOT NULL,
  `id_alternativa` int NOT NULL,
  `tiempo_utilizado` int DEFAULT '0',
  `fecha_respuesta` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_respuesta`),
  UNIQUE KEY `clave_unica_usuario_pregunta` (`id_usuario`,`id_pregunta`),
  KEY `indice_usuario` (`id_usuario`),
  KEY `indice_pregunta` (`id_pregunta`),
  KEY `indice_alternativa` (`id_alternativa`),
  CONSTRAINT `Respuesta_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `Usuario` (`id_usuario`) ON DELETE CASCADE,
  CONSTRAINT `Respuesta_ibfk_2` FOREIGN KEY (`id_pregunta`) REFERENCES `Pregunta` (`id_pregunta`) ON DELETE CASCADE,
  CONSTRAINT `Respuesta_ibfk_3` FOREIGN KEY (`id_alternativa`) REFERENCES `Alternativa` (`id_alternativa`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Respuesta`
--

LOCK TABLES `Respuesta` WRITE;
/*!40000 ALTER TABLE `Respuesta` DISABLE KEYS */;
/*!40000 ALTER TABLE `Respuesta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Usuario`
--

DROP TABLE IF EXISTS `Usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Usuario` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `id_jugador` int DEFAULT NULL,
  `alias` varchar(20) NOT NULL,
  `id_cuestionario` int DEFAULT NULL,
  `puntaje` decimal(5,2) NOT NULL,
  `fecha_participacion` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `uq_usuario_alias_por_cuestionario` (`id_cuestionario`,`alias`),
  CONSTRAINT `Usuario_ibfk_1` FOREIGN KEY (`id_cuestionario`) REFERENCES `Cuestionario` (`id_cuestionario`)
) ENGINE=InnoDB AUTO_INCREMENT=117 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Usuario`
--

LOCK TABLES `Usuario` WRITE;
/*!40000 ALTER TABLE `Usuario` DISABLE KEYS */;
INSERT INTO `Usuario` VALUES (1,2,'anggelo',1,10.00,'2025-11-03 01:52:59'),(2,3,'jsjsjsj',1,15.00,'2025-11-03 01:52:59'),(3,4,'gooo',1,20.00,'2025-11-03 01:52:59'),(4,5,'usuario_1',1,15.00,'2025-11-03 01:52:59'),(5,6,'usuario_2',1,15.00,'2025-11-03 01:52:59'),(6,7,'usuario_3',1,15.00,'2025-11-03 01:52:59'),(7,8,'usuario_4',1,12.00,'2025-11-03 01:52:59'),(8,9,'usuario_5',1,9.00,'2025-11-03 01:52:59'),(9,10,'usuario_6',1,10.00,'2025-11-03 01:52:59'),(10,1,'usuario_7',1,15.00,'2025-11-03 01:52:59'),(11,2,'usuario_8',1,12.00,'2025-11-03 01:52:59'),(12,3,'usuario_9',1,12.00,'2025-11-03 01:52:59'),(13,4,'usuario_10',1,12.00,'2025-11-03 01:52:59'),(14,5,'usuario_11',1,10.00,'2025-11-03 01:52:59'),(15,6,'usuario_12',1,15.00,'2025-11-03 01:52:59'),(16,7,'usuario_13',1,12.00,'2025-11-03 01:52:59'),(17,8,'usuario_14',1,12.00,'2025-11-03 01:52:59'),(18,9,'usuario_15',1,12.00,'2025-11-03 01:52:59'),(19,10,'usuario_16',1,12.00,'2025-11-03 01:52:59'),(20,1,'usuario_17',1,12.00,'2025-11-03 01:52:59'),(21,2,'usuario_18',1,115.00,'2025-11-03 01:52:59'),(22,3,'usuario_19',1,12.00,'2025-11-03 01:52:59'),(23,4,'usuario_20',1,12.00,'2025-11-03 01:52:59'),(24,5,'chuiii',1,13.00,'2025-11-03 01:52:59'),(25,6,'12345',1,0.00,'2025-11-03 01:52:59'),(26,7,'Erick',12,0.00,'2025-11-03 01:52:59'),(27,8,'anggelo',12,0.00,'2025-11-03 01:52:59'),(28,9,'goku',1,0.00,'2025-11-03 01:52:59'),(29,10,'anggelo123',1,0.00,'2025-11-03 01:52:59'),(30,1,'Abraham',12,0.00,'2025-11-03 01:52:59'),(31,2,'Pablidis',12,0.00,'2025-11-03 01:52:59'),(32,3,'Pablo',12,0.00,'2025-11-03 01:52:59'),(33,4,'Pepito',12,0.00,'2025-11-03 01:52:59'),(34,5,'JOSE',12,0.00,'2025-11-03 01:52:59'),(35,6,'asasdasd',12,0.00,'2025-11-03 01:52:59'),(36,7,'a',12,0.00,'2025-11-03 01:52:59'),(37,8,'b',12,0.00,'2025-11-03 01:52:59'),(38,9,'c',12,8.00,'2025-11-03 01:52:59'),(39,10,'CHUIIII',1,0.00,'2025-11-03 01:52:59'),(40,1,'jesus',6,6.67,'2025-11-03 01:52:59'),(41,2,'jesus',11,0.00,'2025-11-03 01:52:59'),(42,3,'jesus',1,0.00,'2025-11-03 01:52:59'),(43,4,'jesus',2,0.00,'2025-11-03 01:52:59'),(44,5,'jesus',3,0.00,'2025-11-03 01:52:59'),(45,6,'jesus2',11,0.00,'2025-11-03 01:52:59'),(46,7,'jesus',12,7.08,'2025-11-03 01:52:59'),(47,8,'gcgc',1,0.00,'2025-11-03 01:52:59'),(48,9,'XD',12,0.00,'2025-11-03 01:52:59'),(49,10,'xdd',12,0.00,'2025-11-03 01:52:59'),(50,1,'xdxdxd',12,4.17,'2025-11-03 01:52:59'),(51,2,'gogo',12,2.50,'2025-11-03 01:52:59'),(52,3,'123QW',12,4.58,'2025-11-03 01:52:59'),(53,4,'QEQE',12,2.08,'2025-11-03 01:52:59'),(54,5,'qwe',1,0.00,'2025-11-03 01:52:59'),(55,6,'qwe31',1,0.00,'2025-11-03 01:52:59'),(56,7,'1234SD',1,0.00,'2025-11-03 01:52:59'),(57,8,'1231EQWD',1,0.00,'2025-11-03 01:52:59'),(58,9,'12312eds',1,0.00,'2025-11-03 01:52:59'),(59,10,'RDS',1,0.00,'2025-11-03 01:52:59'),(60,1,'eksp1',1,0.00,'2025-11-03 01:52:59'),(62,3,'CHUIIII',11,0.00,'2025-11-03 01:52:59'),(65,6,'Elio',11,0.00,'2025-11-03 01:52:59'),(66,NULL,'gcgcg',6,0.00,'2025-11-03 09:41:31'),(67,NULL,'qwe',28,0.00,'2025-11-03 09:45:59'),(68,NULL,'a',26,0.00,'2025-11-03 09:49:29'),(69,NULL,'yy',22,0.00,'2025-11-03 09:53:44'),(70,NULL,'wa',21,0.00,'2025-11-03 09:56:08'),(71,NULL,'raaa',21,0.00,'2025-11-03 09:56:33'),(72,NULL,'121212d',21,0.00,'2025-11-03 13:22:44'),(89,NULL,'chuimix12',44,0.00,'2025-11-04 17:44:19'),(90,NULL,'chuimix16',45,0.00,'2025-11-04 18:01:22'),(91,NULL,'chui12',46,0.00,'2025-11-04 18:30:38'),(92,NULL,'chuimix16',47,0.00,'2025-11-04 19:12:38'),(93,NULL,'chui',48,0.00,'2025-11-04 19:20:35'),(94,NULL,'chuiy1',49,0.00,'2025-11-04 19:29:02'),(95,NULL,'chuimix',50,0.00,'2025-11-04 19:40:50'),(96,NULL,'chumix16',51,0.00,'2025-11-04 19:53:33'),(97,NULL,'casd',52,-1.50,'2025-11-04 19:58:02'),(98,NULL,'chui',55,0.00,'2025-11-04 23:28:21'),(99,16,'chui',56,27.00,'2025-11-11 15:24:29'),(100,NULL,'Chui',57,28.00,'2025-11-12 22:02:34'),(116,NULL,'chu',43,0.00,'2025-11-27 05:36:25');
/*!40000 ALTER TABLE `Usuario` ENABLE KEYS */;
UNLOCK TABLES;

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
  `id_usuario` int NOT NULL COMMENT 'Usuario que vota',
  `id_alternativa` int NOT NULL COMMENT 'Alternativa por la que votó',
  `fecha_votacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_votacion`),
  UNIQUE KEY `unique_grupo_pregunta_usuario` (`id_grupo`,`id_pregunta`,`id_usuario`),
  KEY `id_pregunta` (`id_pregunta`),
  KEY `id_alternativa` (`id_alternativa`),
  KEY `idx_grupo_pregunta` (`id_grupo`,`id_pregunta`),
  KEY `idx_usuario` (`id_usuario`),
  CONSTRAINT `VotacionGrupo_ibfk_1` FOREIGN KEY (`id_grupo`) REFERENCES `Grupo` (`id_grupo`) ON DELETE CASCADE,
  CONSTRAINT `VotacionGrupo_ibfk_2` FOREIGN KEY (`id_pregunta`) REFERENCES `Pregunta` (`id_pregunta`) ON DELETE CASCADE,
  CONSTRAINT `VotacionGrupo_ibfk_3` FOREIGN KEY (`id_usuario`) REFERENCES `Usuario` (`id_usuario`) ON DELETE CASCADE,
  CONSTRAINT `VotacionGrupo_ibfk_4` FOREIGN KEY (`id_alternativa`) REFERENCES `Alternativa` (`id_alternativa`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `VotacionGrupo`
--

LOCK TABLES `VotacionGrupo` WRITE;
/*!40000 ALTER TABLE `VotacionGrupo` DISABLE KEYS */;
/*!40000 ALTER TABLE `VotacionGrupo` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-27  0:48:15
