-- MySQL dump 10.13  Distrib 8.0.41, for Linux (x86_64)
--
-- Host: localhost    Database: control_acceso
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `matriculas`
--

DROP TABLE IF EXISTS `matriculas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `matriculas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `matricula` varchar(10) NOT NULL,
  `estado` enum('pendiente','autorizada','denegada') DEFAULT 'pendiente',
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `matricula` (`matricula`),
  KEY `fk_usuario` (`usuario_id`),
  CONSTRAINT `fk_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `matriculas`
--

LOCK TABLES `matriculas` WRITE;
/*!40000 ALTER TABLE `matriculas` DISABLE KEYS */;
INSERT INTO `matriculas` VALUES (1,'3456CXT','autorizada','2025-03-18 17:27:15',7),(5,'1234ABC','autorizada','2025-04-23 19:28:13',7),(30,'3547NXB','autorizada','2025-05-07 20:48:09',8),(38,'2341SAZ','autorizada','2025-05-13 12:05:07',7),(43,'3435PSD','denegada','2025-05-14 16:16:06',7),(44,'4356MSN','autorizada','2025-05-14 16:16:55',7),(50,'5464DXA','autorizada','2025-05-21 14:39:16',7),(51,'2344ASX','denegada','2025-05-21 14:41:21',7);
/*!40000 ALTER TABLE `matriculas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registros_accesos`
--

DROP TABLE IF EXISTS `registros_accesos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registros_accesos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `matricula` varchar(10) NOT NULL,
  `estado` enum('pendiente','autorizada','denegada') DEFAULT NULL,
  `fecha` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `imagen` varchar(255) DEFAULT NULL,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `matricula` (`matricula`),
  KEY `fk_registros_usuario` (`usuario_id`),
  CONSTRAINT `fk_registros_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `registros_accesos_ibfk_1` FOREIGN KEY (`matricula`) REFERENCES `matriculas` (`matricula`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=127 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registros_accesos`
--

LOCK TABLES `registros_accesos` WRITE;
/*!40000 ALTER TABLE `registros_accesos` DISABLE KEYS */;
INSERT INTO `registros_accesos` VALUES (122,'1234ABC','autorizada','2025-05-15 08:00:00',NULL,7),(123,'1234ABC','autorizada','2025-05-15 09:00:00',NULL,7),(124,'1234ABC','autorizada','2025-05-16 10:00:00',NULL,7),(125,'1234ABC','autorizada','2025-05-17 11:00:00',NULL,7),(126,'1234ABC','autorizada','2025-05-17 14:00:00',NULL,7);
/*!40000 ALTER TABLE `registros_accesos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) DEFAULT NULL,
  `apellidos` varchar(100) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `rol` varchar(20) DEFAULT 'usuario',
  `foto` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (7,'prueba','prueba','prueba@prueba.com','scrypt:32768:8:1$yPpjBMAmLvthwoJG$69b477d2396c3a7fe6d3d679413a24acdc3bef7f0b47f5110b8913af246d12405322daa1dbbcedf76072e1ed23ad751c70e9e556a62b50cfd3ea5157cb1be493','usuario','user_7.png'),(8,'Admin','Principal','admin@admin.com','scrypt:32768:8:1$mFvn0IhJXhKnZ2FA$8dc6977671c39847253ca7050173cf174b377dc0f03761a75eb694826a573203935cba19e0cd8c5f9a04454682e255754372a9c9b7df3efb5d8d7905959e3116','admin',NULL),(17,'Gigante','Mental','gigante@gmail.com','scrypt:32768:8:1$CazoelHZyi3rX15W$c4d43e57bad35297630bb74d7bbbe6ad9cee3d227e5db9f50d69ec1f7585b53fe080a8ae6065038e8a8c5be88108c3bbb522f6eceaa2bbac5cdce2b1924ec89a','usuario',NULL);
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

-- Dump completed on 2025-05-27 16:03:18
