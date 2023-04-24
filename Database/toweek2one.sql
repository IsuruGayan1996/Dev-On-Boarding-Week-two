-- MySQL dump 10.13  Distrib 8.0.32, for Linux (x86_64)
--
-- Host: localhost    Database: toweek2one
-- ------------------------------------------------------
-- Server version	8.0.32-0ubuntu0.22.04.2

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
-- Table structure for table `pins`
--

DROP TABLE IF EXISTS `pins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pins` (
  `pin_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(50) DEFAULT NULL,
  `body` varchar(100) DEFAULT NULL,
  `image` varchar(150) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `added_date` date DEFAULT NULL,
  PRIMARY KEY (`pin_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `pins_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pins`
--

LOCK TABLES `pins` WRITE;
/*!40000 ALTER TABLE `pins` DISABLE KEYS */;
INSERT INTO `pins` VALUES (1,'pin1','SSSSSSSSSSSSSS','Screenshot_from_2023-04-20_09-41-16.png',2,'2023-04-22'),(3,'Pin3','Hello2','image.png',5,'2023-04-23'),(4,'pin1','Hello1','Screenshot_from_2023-04-20_21-41-41.png',5,'2023-04-23'),(6,'pin1','Hello1','Screenshot_from_2023-04-20_21-41-41.png',11,'2023-04-24'),(7,'pin1','Hello1','Screenshot_from_2023-04-20_21-41-41.png',11,'2023-04-24'),(9,'pin1','Hello1','Screenshot_from_2023-04-20_21-41-41.png',11,'2023-04-24'),(10,'pin1','Hello1','Screenshot_from_2023-04-20_21-41-41.png',11,'2023-04-24'),(11,'pin1','Hello1','Screenshot_from_2023-04-20_21-41-41.png',11,'2023-04-24'),(12,'Pin4','Hello2','image.png',11,'2023-04-25'),(13,'pin1','Hello1','Screenshot_from_2023-04-20_21-41-41.png',11,'2023-04-24'),(14,'pin1','Hello1','Screenshot_from_2023-04-20_21-41-41.png',11,'2023-04-25');
/*!40000 ALTER TABLE `pins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `refresh_tokens`
--

DROP TABLE IF EXISTS `refresh_tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `refresh_tokens` (
  `user_id` int DEFAULT NULL,
  `refresh_token` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `refresh_tokens`
--

LOCK TABLES `refresh_tokens` WRITE;
/*!40000 ALTER TABLE `refresh_tokens` DISABLE KEYS */;
INSERT INTO `refresh_tokens` VALUES (2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyfQ.xLtLz4_IFNJ71dV0y0lu8WwOPdy87UFBr9PsTsIxBDU'),(2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyfQ.xLtLz4_IFNJ71dV0y0lu8WwOPdy87UFBr9PsTsIxBDU'),(2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyfQ.xLtLz4_IFNJ71dV0y0lu8WwOPdy87UFBr9PsTsIxBDU'),(5,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo1fQ.ti8-vMuowE-GvVhai9np182VVWG38aQqFKHTv1G5ylQ'),(11,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMX0.Y6KD83e-W4fO7xVl5KO1UbKAaCRqvrnUJ1OLIT-OWj8'),(11,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMX0.Y6KD83e-W4fO7xVl5KO1UbKAaCRqvrnUJ1OLIT-OWj8'),(11,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMX0.Y6KD83e-W4fO7xVl5KO1UbKAaCRqvrnUJ1OLIT-OWj8'),(5,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo1fQ.ti8-vMuowE-GvVhai9np182VVWG38aQqFKHTv1G5ylQ'),(5,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo1fQ.ti8-vMuowE-GvVhai9np182VVWG38aQqFKHTv1G5ylQ'),(5,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo1fQ.ti8-vMuowE-GvVhai9np182VVWG38aQqFKHTv1G5ylQ'),(5,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo1fQ.ti8-vMuowE-GvVhai9np182VVWG38aQqFKHTv1G5ylQ');
/*!40000 ALTER TABLE `refresh_tokens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'Nethmi','nethmi27@gmail.com','sha256$wokmUMw6XOfMV5en$5cfd030b6a22cc9c8a8f7484f9dfc4180462b4d62d8cf57936e1dee7d4e33cef'),(5,'Ishan','ishanm28@gmail.com','sha256$O5lv94D5evnf3S1E$c978d944e510677d4efe6725ac133a79f5b34e82284d1d7e383b41e3d98ecbbc'),(11,'milindaaa','ishanm28@gmail.com','sha256$0mzN9nqXEfnd16y4$6e0b613295141bf696e7c44b57a085b713803403ac6d09dc8626a81694bce162'),(12,'Gimhann','milinda27@gmail.com','sha256$5PBRLIrXi6FUxgWw$4599eda6f8b35f31bb789182dc6599730ff91d3d47714ad70c6dc2372c1835cb'),(13,'Gimhannn','milinda27@gmail.com','sha256$Gv1QSI3kjwPMH4wa$3ead7f8fb71f04841b970df4e3a15f73f9e1c83f95f4569665394c351d5e49de'),(15,'Samitha','milinda27@gmail.com','sha256$MRFs9WlfM7AjDnYy$847d573fa9bf5a410d8394b99186391b3a4a112fa138c64415c1d788a4ab7568');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-25  0:46:32
