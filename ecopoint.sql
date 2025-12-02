CREATE DATABASE  IF NOT EXISTS `ecopoint` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `ecopoint`;
-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: ecopoint
-- ------------------------------------------------------
-- Server version	9.4.0

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
-- Table structure for table `clasificacion`
--

DROP TABLE IF EXISTS `clasificacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clasificacion` (
  `id_clasificacion` int NOT NULL AUTO_INCREMENT,
  `id_material` int DEFAULT NULL,
  `sugerencia` varchar(50) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `comentario_gestor` text,
  `fecha_registro` datetime NOT NULL,
  PRIMARY KEY (`id_clasificacion`),
  KEY `id_material` (`id_material`),
  CONSTRAINT `clasificacion_ibfk_1` FOREIGN KEY (`id_material`) REFERENCES `material` (`id_material`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clasificacion`
--

LOCK TABLES `clasificacion` WRITE;
/*!40000 ALTER TABLE `clasificacion` DISABLE KEYS */;
INSERT INTO `clasificacion` VALUES (1,1,'Vidrio','Aceptada','Perfecto','2025-12-01 13:19:03'),(2,2,'Cartón','Aceptada','nice','2025-12-01 13:20:16'),(3,3,'Cartón','Rechazada','No puede tener categoria de carton, debe reciclarse como plastico','2025-12-01 13:22:01'),(4,4,'PET 1 (Limpio)','Aceptada','perfecto','2025-12-01 15:46:35');
/*!40000 ALTER TABLE `clasificacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `material`
--

DROP TABLE IF EXISTS `material`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `material` (
  `id_material` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int DEFAULT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  `cantidad` decimal(10,2) DEFAULT NULL,
  `peso` decimal(10,2) DEFAULT NULL,
  `estado` varchar(50) DEFAULT NULL,
  `fotografia` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_material`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `material_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `material`
--

LOCK TABLES `material` WRITE;
/*!40000 ALTER TABLE `material` DISABLE KEYS */;
INSERT INTO `material` VALUES (1,1,'Vidrio',1.00,5.00,'Triturado',NULL),(2,1,'Carton',6.00,1.20,'Sucio',NULL),(3,1,'platico',8.00,0.20,'Mezclado',NULL),(4,1,'Plastico',70.00,1.00,'Mezclado',NULL);
/*!40000 ALTER TABLE `material` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `procesotransformacion`
--

DROP TABLE IF EXISTS `procesotransformacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `procesotransformacion` (
  `id_proceso` int NOT NULL AUTO_INCREMENT,
  `id_material` int DEFAULT NULL,
  `etapa` varchar(50) DEFAULT NULL,
  `fecha_registro` datetime DEFAULT NULL,
  PRIMARY KEY (`id_proceso`),
  KEY `id_material` (`id_material`),
  CONSTRAINT `procesotransformacion_ibfk_1` FOREIGN KEY (`id_material`) REFERENCES `material` (`id_material`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `procesotransformacion`
--

LOCK TABLES `procesotransformacion` WRITE;
/*!40000 ALTER TABLE `procesotransformacion` DISABLE KEYS */;
INSERT INTO `procesotransformacion` VALUES (1,3,'Clasificación','2025-12-01 20:25:56'),(2,3,'Trituración','2025-12-01 20:26:13'),(3,4,'Clasificación','2025-12-01 20:48:19'),(4,4,'Trituración','2025-12-01 20:48:28'),(5,4,'Lavado','2025-12-01 20:48:37');
/*!40000 ALTER TABLE `procesotransformacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reporte`
--

DROP TABLE IF EXISTS `reporte`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reporte` (
  `id_reporte` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int DEFAULT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  PRIMARY KEY (`id_reporte`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `reporte_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reporte`
--

LOCK TABLES `reporte` WRITE;
/*!40000 ALTER TABLE `reporte` DISABLE KEYS */;
/*!40000 ALTER TABLE `reporte` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `contrasena` varchar(255) DEFAULT NULL,
  `rol` varchar(50) NOT NULL,
  `puntos` int DEFAULT '0',
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'Patrick','patrickacalderon@gmail.com','pbkdf2_sha256$1000000$qXTN0aUbQPP3f2JXipXB7N$wmyx1aDHD4OTxhJtC5Pxm4aO2g3GrRZUnogF0wKSfCA=','usuario',55),(2,'Editado','123@sass','pbkdf2_sha256$1000000$pquLWhJ57HgU1iwcg4lkpw$iV7ZZQ0k2cVOYeXTcjoaTY9RG4DPYKHwgSQlMPA2QFU=','usuario',0),(3,'asdad','1111@gmail.com','pbkdf2_sha256$1000000$6bq2iit0RblfGSirVPZ3fJ$fRD8qTO2U1mSlyrwbQ3zKdw0zV4QDHq9AvLFoDMBfMk=','usuario',0),(4,'Administrador','admin@admin.com','pbkdf2_sha256$1000000$bZZMdWPFsxokfXOoQ6azKG$JLu+FUe3XbSl9A6y1IfCQAuMCn7u2bB/6Hv4AkQRgXw=','admin',0),(5,'Patrick Calderon','abcde@gmail.com','pbkdf2_sha256$1000000$g2tt4B6M4HDaeoRIZct1x4$ju2nfWOepc0HC7RlHY+avo2TzfeysgGZzkAQsa+brHI=','usuario',0);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-01 19:42:24
