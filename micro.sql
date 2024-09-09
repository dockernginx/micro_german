-- MySQL dump 10.13  Distrib 8.0.39, for Linux (x86_64)
--
-- Host: localhost    Database: microservicios
-- ------------------------------------------------------
-- Server version	8.0.39-0ubuntu0.24.04.2

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
-- Table structure for table `clases`
--

DROP TABLE IF EXISTS `clases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clases` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_clase` varchar(255) NOT NULL,
  `profesor` varchar(255) NOT NULL,
  `horario` varchar(255) DEFAULT NULL,
  `aula` varchar(255) DEFAULT NULL,
  `calificacion` decimal(3,2) DEFAULT NULL,
  `semestre` int NOT NULL,
  `descripcion` text,
  `estudiante_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `estudiante_id` (`estudiante_id`),
  CONSTRAINT `clases_ibfk_1` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiantes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `clases_chk_1` CHECK (((`calificacion` >= 0) and (`calificacion` <= 10)))
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clases`
--

LOCK TABLES `clases` WRITE;
/*!40000 ALTER TABLE `clases` DISABLE KEYS */;
INSERT INTO `clases` VALUES (1,'Física Moderna','Dra. María Gómez','Jueves 14:00 - 16:00','B202',9.50,5,'Clase avanzada de física moderna y relatividad',1),(2,'Matemáticas','Dr. Juan Pérez','Lunes 9:00 - 11:00','A101',8.50,3,'Clase de matemáticas avanzadas',1),(3,'Física','Dra. María Gómez','Martes 10:00 - 12:00','B202',9.00,4,'Clase introductoria a la física moderna',2),(4,'Historia','Dra. Laura Sánchez','Jueves 14:00 - 16:00','D404',8.90,5,'Historia universal',1),(5,'Biología','Dr. José López','Viernes 8:00 - 10:00','E505',9.20,3,'Biología celular y molecular',4),(6,'Geografía','Dra. Clara Rivas','Lunes 11:00 - 13:00','F606',8.30,2,'Geografía física y política',2),(7,'Programación','Dr. Alberto Pérez','Martes 9:00 - 11:00','G707',9.50,4,'Introducción a la programación en Python',3),(8,'Economía','Dra. Ana Torres','Viernes 12:00 - 14:00','H808',8.00,5,'Fundamentos de economía',4);
/*!40000 ALTER TABLE `clases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estudiantes`
--

DROP TABLE IF EXISTS `estudiantes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estudiantes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email_or_username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `numero_control` varchar(50) NOT NULL,
  `carrera` varchar(255) DEFAULT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `grupo` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_or_username` (`email_or_username`),
  UNIQUE KEY `numero_control` (`numero_control`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estudiantes`
--

LOCK TABLES `estudiantes` WRITE;
/*!40000 ALTER TABLE `estudiantes` DISABLE KEYS */;
INSERT INTO `estudiantes` VALUES (1,'lucia@gmail.com','$2b$12$vlu5TSrhQl.jDS0TO/1dGO.cM24Od2l1LQ8P5aKZ7T88g33mZcDYO','Lucia Luego','123456782','Licenciatura en Diseño Digital','2024-09-08 22:36:27','GIDI4091'),(2,'Luc@gmail.com','$2b$12$mWEGgosRATh8Xdiqj8ur/O3K6uau80S7dWlDHV8oj3ur6Y6SimE82','Luci Lugo','12345682','Ingeniería en Sistemas','2024-09-08 22:39:05','IGSIS4590'),(3,'juanp@gmail.com','$2b$12$CvrISla9JhuBB/tvBjCE6uKOAYeMJGnj5n3WxOlT1PWo1mJRj4cVe','Juan Pérez','12345683','Ingeniería en Software','2024-09-09 04:11:49','IGSIS4591'),(4,'mariaj@gmail.com','$2b$12$Rv7Y817mZ2phNS6rBIG3T.mhdY92NA94YyqD7sdo7aOwY5ATyvsKG','María Jiménez','12345684','Ingeniería en Sistemas','2024-09-09 04:12:04','IGSIS4592'),(5,'carlosr@gmail.com','$2b$12$YtPRx7LxVnZlJqeyJWGFHeqB1d6fvrRbXy8ZLlHZx85G0933bR.9a','Carlos Rodríguez','12345685','Ciencia de Datos','2024-09-09 04:12:22','IGSIS4593'),(6,'andream@gmail.com','$2b$12$7BFV5MuRs4wjP3KlIBYd/OAzDZWcIkVIRQqGf4hxAYHzw3apcA/gq','Andrea Martínez','12345686','Ingeniería en Sistemas','2024-09-09 04:12:32','IGSIS4594'),(7,'pedrol@gmail.com','$2b$12$0p1SG1.wq/GOyxN2cJIPlOpVExRGz1CqXr41a/9J86xEK09OCc7C6','Pedro López','12345687','Ingeniería en Software','2024-09-09 04:12:43','IGSIS4595'),(8,'sofiag@gmail.com','$2b$12$FdFxoFEA7IfPEsEYyreKPejaPaQ3sZI4/DtytIrlomUnIUQw2KTOm','Sofía García','12345688','Ingeniería en Sistemas','2024-09-09 04:13:07','IGSIS4596'),(9,'alejandroc@gmail.com','$2b$12$LhNnE.ZqmPbkPbYuFqGisuQJVKlNxaWbzZqSKI7okaHvG24AHfEQ2','Alejandro Cruz','12345689','Ingeniería en Telecomunicaciones','2024-09-09 04:13:17','IGSIS4597'),(10,'laurag@gmail.com','$2b$12$3x0Ruh0G.DgmZNSuB2YbXOJfj01NqSe9o7Wn8zPp/dmghtKsEB2Ru','Laura González','12345690','Ingeniería en Software','2024-09-09 04:14:07','IGSIS4598');
/*!40000 ALTER TABLE `estudiantes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-08 22:29:35
