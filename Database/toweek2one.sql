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
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pins`
--

LOCK TABLES `pins` WRITE;
/*!40000 ALTER TABLE `pins` DISABLE KEYS */;
INSERT INTO `pins` VALUES (32,'pin1','pin1_body','sample_image1.png',16,'2023-04-26'),(33,'pin2','pin2_body','sample_image1.png',16,'2023-04-26'),(34,'pin3','pin3_body','sample_image1.png',16,'2023-04-26'),(35,'pin4','pin4_body','sample_image1.png',16,'2023-04-26'),(36,'pin5','pin5_body','sample_image1.png',16,'2023-04-26'),(37,'pin5','pin5_body','sample_image1.png',25,'2023-04-26'),(38,'pin4','pin4_body','sample_image2.png',25,'2023-04-26'),(39,'pin3','pin3_body','sample_image2.png',25,'2023-04-26'),(40,'pin2','pin2_body','sample_image2.png',25,'2023-04-26'),(41,'pin1','pin1_body','sample_image2.png',25,'2023-04-26');
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
INSERT INTO `refresh_tokens` VALUES (16,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwiZXhwIjoxNjgzMDA2MjE2fQ.I1RnBAyImuxpljAiPHYYig-RlLc7n3XaQZ_TTH2DwnQ'),(16,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwiZXhwIjoxNjgzMDA2Mjc3fQ.yqWVxj4uPk2UWV4BxoIRwMPB0MocKv7NBWO9SMglj30'),(16,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwiZXhwIjoxNjgzMDA5MzcyfQ.9L8KfGshgVQ05_7kep2cpsj2lgK_mrvMSUTf8_MVpnE'),(16,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwiZXhwIjoxNjgzMDI2MTYzfQ.BimGWVIUYIlYwNucOkufTAlwXOw6pK5SCVJi966SQ0Q'),(16,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwiZXhwIjoxNjgzMDI2MTc3fQ.xi9vxUn7OKtO7TSRaj89fGeOI4eRYOMessmnmPJX8Zg'),(16,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwiZXhwIjoxNjgzMDI2Mjg4fQ.ellulMkyG-YenTZwflN8uqL_p8nji6kkIQXE8O1RsGM'),(25,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyNSwiZXhwIjoxNjgzMDI2NTg1fQ.beZRLbKaIOmIbsrGACYoK2ARWGgnyO41O9_Ul6LaXik'),(25,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyNSwiZXhwIjoxNjgzMDQ2MDU0fQ.JqlOxalDRaqawkElDi0pmRHU92Hvv0rqizawa0LQlHA'),(16,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwiZXhwIjoxNjgzMDg2MzM2fQ.1llJSlFSiuI6WMh10FltIb5kreS-v5ohuEaKQ39uyGQ'),(25,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyNSwiZXhwIjoxNjgzMDg2NDE0fQ.juzayIXFkm75GaKOxA7ZQ0d1QhNueoAcj1j_UABY_eA');
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
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (16,'example_user1','example_user1@gmail.com','sha256$U7FgIQSf9j26Gl2x$b7f4cc7b1b2892b870861d9fee58535beac965cf90b5008c35ee700173601dfc'),(17,'example_user2','example_user2@gmail.com','sha256$VRyXX3k1OF7FIIfB$a941912cbecbb7192349599395f679c35b47cbeb8af22b58d71383b6a7f4076b'),(18,'example_user3','example_user3@gmail.com','sha256$UZUzksUJUr2SNdey$493d19a07a13820cd58abb22a9502a2778df355cdc58cb9b6e4784bb836022f0'),(19,'example_user4','example_user4@gmail.com','sha256$4whQi7z0l7mBknVm$592951bc0cda45d917c149221be62c976c41121f57f701787cba991c25364e75'),(20,'example_user5','example_user5@gmail.com','sha256$YPLMwcjgFrcVUvyB$f992a0d56700cbaf22c5bac249544d8c096fc3f7b084f9a59c1270dc075724cb'),(21,'example_user6','example_user6@gmail.com','sha256$LVmUsptlHLTP9vT1$4d406b5e5abd963d35d94d508128e54718ec8b7551a61175a0b308f7a1de5c9a'),(22,'example_user7','example_user7@gmail.com','sha256$aC5HtuwoD4FOx2tI$18795826e5dfad062d04f8ee4235828f51fede4407c78c69f5a142d860af1c0c'),(23,'example_user8','example_user8@gmail.com','sha256$DNWqw0pT2IoJ2Eo3$cbac960fdbc5c964a2a9f834b1bcfc3cb2b66d94fece11bfff3dd6b4394bf0e7'),(24,'example_user9','example_user9@gmail.com','sha256$QGPAaQR8B0ZQLrMJ$ab78824db2a33e1bf5e5c26b713b9c0932145968d52b564c9e75d99b2cfe563a'),(25,'example_user10','example_user10@gmail.com','sha256$Lb3oXOhj4Ljsyjgg$d823c7a02f9d18fa2043cb3a78f1f53aa4a9d3986ec5d97baa23cab68635f893'),(26,'example_user11','example_user11gmail.com','sha256$nKeSrDzD7o55G1p8$0d5bdcc7e86e96a5b9b10e6ea550eb02be4820f92e7e153c31d258a9afcdf3b9');
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

-- Dump completed on 2023-04-26  9:31:40
