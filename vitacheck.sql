-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: db_parcial
-- ------------------------------------------------------
-- Server version	8.0.46

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

--
-- Table structure for table `categorias`
--

DROP TABLE IF EXISTS `categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias` (
  `idCategoria` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `rangoMin` float NOT NULL,
  `rangoMax` float NOT NULL,
  `recomendacion` text NOT NULL,
  PRIMARY KEY (`idCategoria`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias`
--

LOCK TABLES `categorias` WRITE;
/*!40000 ALTER TABLE `categorias` DISABLE KEYS */;
INSERT INTO `categorias` VALUES (1,'Bajo peso',0,18.49,'Bajo peso. Se sugiere aumentar el consumo calórico con nutrientes saludables.'),(2,'Normal',18.5,24.99,'Peso normal. Mantener una dieta equilibrada y actividad constante.'),(3,'Sobrepeso',25,29.99,'Sobrepeso. Reducir azúcares y grasas, acompañado de ejercicio regular.'),(4,'Obesidad I',30,34.99,'Obesidad Grado I. Se recomienda plan de entrenamiento cardiovascular y control nutricional.'),(5,'Obesidad II',35,39.99,'Obesidad Grado II. Es crucial consultar con un especialista médico para ajustar hábitos.'),(6,'Obesidad III',40,999,'Obesidad Grado III (Mórbida). Requiere intervención médica e integral inmediata.');
/*!40000 ALTER TABLE `categorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `citas`
--

DROP TABLE IF EXISTS `citas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `citas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `paciente_id` int NOT NULL,
  `medico_id` int NOT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `estado` enum('pendiente','programada','completada','cancelada') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'pendiente',
  `motivo` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `paciente_id` (`paciente_id`),
  KEY `medico_id` (`medico_id`),
  KEY `fecha` (`fecha`),
  KEY `estado` (`estado`),
  CONSTRAINT `citas_ibfk_1` FOREIGN KEY (`paciente_id`) REFERENCES `pacientes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `citas_ibfk_2` FOREIGN KEY (`medico_id`) REFERENCES `medicos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `citas`
--

LOCK TABLES `citas` WRITE;
/*!40000 ALTER TABLE `citas` DISABLE KEYS */;
INSERT INTO `citas` VALUES (1,4,3,'2026-01-03','13:22:00','cancelada','le duele el dedo pequeño del pie izquierdo','2025-11-23 05:21:29'),(2,11,2,'2026-05-12','06:49:00','completada','algo','2026-05-27 23:50:00'),(3,1,8,'2026-06-10','15:14:00','pendiente','dolor de pierna fuerte','2026-05-28 05:14:26');
/*!40000 ALTER TABLE `citas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `especialidades`
--

DROP TABLE IF EXISTS `especialidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `especialidades` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `especialidades`
--

LOCK TABLES `especialidades` WRITE;
/*!40000 ALTER TABLE `especialidades` DISABLE KEYS */;
INSERT INTO `especialidades` VALUES (1,'Medicina General','Atención primaria'),(2,'Cardiología','Especialidad cardiovascular'),(3,'Pediatría','Atención a niños');
/*!40000 ALTER TABLE `especialidades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historias_clinicas`
--

DROP TABLE IF EXISTS `historias_clinicas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historias_clinicas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `paciente_id` int NOT NULL,
  `medico_id` int DEFAULT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `nota` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `tipo` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `paciente_id` (`paciente_id`),
  KEY `medico_id` (`medico_id`),
  CONSTRAINT `historias_clinicas_ibfk_1` FOREIGN KEY (`paciente_id`) REFERENCES `pacientes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `historias_clinicas_ibfk_2` FOREIGN KEY (`medico_id`) REFERENCES `medicos` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historias_clinicas`
--

LOCK TABLES `historias_clinicas` WRITE;
/*!40000 ALTER TABLE `historias_clinicas` DISABLE KEYS */;
INSERT INTO `historias_clinicas` VALUES (1,1,2,'2025-11-22 23:31:46','la consulta es por que la señora presenta fuertes dolores de cabeza y vomito constante','consulta general','2025-11-23 04:31:46'),(2,11,2,'2026-05-27 18:58:37','hfdño8ew oinge oinrgd oindgoijn','Consulta','2026-05-27 23:58:37');
/*!40000 ALTER TABLE `historias_clinicas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `imc_historial`
--

DROP TABLE IF EXISTS `imc_historial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `imc_historial` (
  `id` int NOT NULL AUTO_INCREMENT,
  `paciente_id` int NOT NULL,
  `peso` decimal(5,2) NOT NULL,
  `altura` decimal(4,2) NOT NULL,
  `imc` decimal(5,2) NOT NULL,
  `clasificacion` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `paciente_id` (`paciente_id`),
  CONSTRAINT `imc_historial_ibfk_1` FOREIGN KEY (`paciente_id`) REFERENCES `pacientes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imc_historial`
--

LOCK TABLES `imc_historial` WRITE;
/*!40000 ALTER TABLE `imc_historial` DISABLE KEYS */;
INSERT INTO `imc_historial` VALUES (1,4,62.00,1.70,21.45,'normal','2025-11-23 14:51:42'),(2,4,64.00,1.70,22.15,'normal','2025-11-23 15:02:24'),(3,6,72.00,1.67,25.82,'alto','2025-11-23 15:05:20'),(4,3,78.00,1.80,24.07,'normal','2025-11-23 15:26:04'),(5,1,80.00,1.89,22.40,'normal','2025-11-23 15:38:47'),(6,2,67.00,1.69,23.46,'normal','2025-11-23 16:05:49'),(7,2,70.00,1.73,23.39,'normal','2025-11-23 16:18:12'),(8,1,70.00,1.80,21.60,'normal','2025-11-23 17:46:15'),(9,9,75.00,1.82,22.64,'normal','2025-11-23 18:12:34'),(10,9,75.00,1.82,22.64,'normal','2025-11-23 18:12:34'),(11,10,35.00,1.35,19.20,'normal','2025-11-23 18:51:36'),(12,10,40.00,1.20,27.78,'alto','2025-11-23 18:52:44'),(13,11,80.00,1.67,28.69,'alto','2025-11-23 18:55:23'),(14,11,70.00,1.82,21.13,'normal','2025-11-23 22:06:07'),(15,6,69.00,1.68,24.45,'normal','2025-11-23 22:07:00'),(16,1,80.00,1.89,22.40,'normal','2025-11-23 22:07:23'),(17,3,70.00,1.79,21.85,'normal','2025-11-23 22:19:24'),(18,4,69.00,1.70,23.88,'normal','2025-11-23 22:35:05'),(19,9,80.00,1.67,28.69,'alto','2025-11-23 22:55:06'),(20,10,40.00,1.20,27.78,'alto','2025-11-23 23:02:42'),(21,11,70.00,1.75,22.86,'normal','2026-05-27 23:53:49'),(22,11,80.00,1.65,29.38,'Sobrepeso','2026-05-28 03:40:30'),(23,11,90.00,1.65,33.06,'Obesidad I','2026-05-28 03:45:42'),(24,11,90.00,1.65,33.06,'Obesidad I','2026-05-28 03:46:18'),(25,11,90.00,1.65,33.06,'Obesidad I','2026-05-28 03:50:38'),(26,11,90.00,1.65,33.06,'Obesidad I','2026-05-28 03:53:23'),(27,11,90.00,1.65,33.06,'Obesidad I','2026-05-28 03:56:02'),(28,13,90.00,1.75,29.39,'Sobrepeso','2026-05-28 04:32:02'),(29,13,90.00,1.75,29.39,'Sobrepeso','2026-05-28 04:32:17'),(30,2,90.00,1.75,29.39,'Sobrepeso','2026-05-28 05:27:28');
/*!40000 ALTER TABLE `imc_historial` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicos`
--

DROP TABLE IF EXISTS `medicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `numero_licencia` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `specialty_id` int NOT NULL,
  `telefono` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_licencia` (`numero_licencia`),
  KEY `specialty_id` (`specialty_id`),
  CONSTRAINT `medicos_ibfk_1` FOREIGN KEY (`specialty_id`) REFERENCES `especialidades` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicos`
--

LOCK TABLES `medicos` WRITE;
/*!40000 ALTER TABLE `medicos` DISABLE KEYS */;
INSERT INTO `medicos` VALUES (1,'Dra. Laura Pérez','LIC-1001',1,'+57 3001112222','laura.perez@clinica.com','2025-11-23 02:09:11'),(2,'Dr. Carlos Gómez','LIC-1002',2,'+57 3003334444','carlos.gomez@clinica.com','2025-11-23 02:09:11'),(3,'Dr. Luis Galan','Lic - 1003',3,'+57 3165332277','luis.galan@clinica.com','2025-11-23 05:20:12'),(8,'jhonatan ','LIC-989',1,'3212521232','jhonatanacevedog@gmail.com','2026-05-28 05:13:32');
/*!40000 ALTER TABLE `medicos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mensajes`
--

DROP TABLE IF EXISTS `mensajes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mensajes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `contenido` text NOT NULL,
  `fechaEnvio` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `leido` tinyint DEFAULT '0',
  `remitente_id` int NOT NULL,
  `destinatario_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `remitente_id` (`remitente_id`),
  KEY `destinatario_id` (`destinatario_id`),
  CONSTRAINT `mensajes_ibfk_1` FOREIGN KEY (`remitente_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `mensajes_ibfk_2` FOREIGN KEY (`destinatario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mensajes`
--

LOCK TABLES `mensajes` WRITE;
/*!40000 ALTER TABLE `mensajes` DISABLE KEYS */;
INSERT INTO `mensajes` VALUES (1,'hola doc como estas.?','2026-05-28 04:35:43',0,1,2),(2,'hola muy buenas noches dr jhonatan','2026-05-28 04:43:04',1,1,3),(3,'hola amigo','2026-05-28 05:15:24',1,1,20),(4,'hola muy buenas noches en que e puedo coaborar.?','2026-05-28 05:20:47',1,3,1),(5,'tengo un dolor de muela que no me deja dormir','2026-05-28 05:25:07',0,1,3),(6,'hi','2026-05-28 05:25:44',1,20,1),(7,'hello','2026-05-28 05:25:52',0,20,2),(8,'hola como estas','2026-05-28 05:26:04',0,20,3),(9,'how are you mrt.?','2026-05-28 05:26:25',1,1,20),(10,'very good very good','2026-05-28 05:26:47',0,20,1);
/*!40000 ALTER TABLE `mensajes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pacientes`
--

DROP TABLE IF EXISTS `pacientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pacientes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `documento` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `telefono` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `direccion` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `genero` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `grupo_sanguineo` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `alergias` varchar(70) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `documento` (`documento`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pacientes`
--

LOCK TABLES `pacientes` WRITE;
/*!40000 ALTER TABLE `pacientes` DISABLE KEYS */;
INSERT INTO `pacientes` VALUES (1,'Juan Torres','CC123456','1985-04-10','+57 3121112211','juan.t@example.com','Calle 1 #2-3','2025-11-23 02:09:18','','',NULL),(2,'María López','CC987654','1992-11-01','+57 3122223333','maria.l@example.com','Calle 4 #5-6','2025-11-23 02:09:18','','',NULL),(3,'sebastian anteliz','10913812','2005-02-08','3187935793','afdazajaimes@gmail.com','nnurt','2025-11-23 05:03:33','','',NULL),(4,'heydi','123456789','2000-02-23','123456789','nojoda@gmail.com','olaquehace13432312','2025-11-23 05:14:08','','',NULL),(6,'Luisa Fabiola Jaimes','1090381227','1987-06-01','3184826517','luisafjaimes@gmail.com','antigua via bocono, urb el cuji','2025-11-23 15:04:37','','',NULL),(9,'pablo emilio escobar','129235349','2001-06-12','3184826517','elpatrondelmal@gmail.com','la hacienda napoles','2025-11-23 18:12:05','','',NULL),(10,'jose angel delgado','123132654','2017-06-15','3184258654','josealderan@gmail.com','nn','2025-11-23 18:50:28','','',NULL),(11,'edinson caravello','19872345','2014-06-10','3156444837','nosequeponer@gmail.com','supernn','2025-11-23 18:54:59','Masculino','A-','a la cerveza'),(13,'jhjgfddf','1004515626','2001-02-02','3243243242','jhonatanacevedog@gmail.com','3242343','2026-05-28 04:31:31','Masculino','O+','');
/*!40000 ALTER TABLE `pacientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'admin'),(3,'medico'),(2,'recepcion');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre_completo` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `role_id` int NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'admin','scrypt:32768:8:1$K7P25Goddxru7aP0$708733622387cc37d1baf39449979779e9d2be4b20891529143519562b60e3f60ccd52ecc29cf09acb9065a011b7d59800536a52ee508a64c44ac476d2dab0dc','Administrador',1,'2025-11-23 04:26:43'),(2,'drperez','scrypt:32768:8:1$7M4wXq6vGZ9... (o cualquier hash válido)','Dr. Carlos Pérez',2,'2026-05-28 04:34:55'),(3,'drjhonatan','scrypt:32768:8:1$7jIE77Y0PT4nQA4h$a085153053203ee090770d343a21a7e6ecb8464a5ef179cc28614fe1b7877aab86180cc35ac5a1641a0378799a484d830a2a22251ad912bd786b8c0c6cf89f4c','Dr. Carlos Pérez',2,'2026-05-28 04:42:26'),(20,'dr.jhon','scrypt:32768:8:1$pJRXjosKyCpkXjot$34d815cd4c1af295e2ff86e67f60fc11e88c09428c102677a75e211417f19220a423576ad708faff442a37fd36b4be7cafb6c7255a91d5063556ae5d7b36df3c','Nombre Apellido',1,'2026-05-28 05:15:00');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-28  0:32:06
