-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: spendwise
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `expenses`
--

DROP TABLE IF EXISTS `expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expenses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `category` varchar(100) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `expenses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=154 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expenses`
--

LOCK TABLES `expenses` WRITE;
/*!40000 ALTER TABLE `expenses` DISABLE KEYS */;
INSERT INTO `expenses` VALUES (1,'2025-10-01','food',387.00,1),(2,'2025-10-01','travel',288.00,1),(3,'2025-10-01','entertainment',195.00,1),(4,'2025-10-01','healthcare',236.00,1),(5,'2025-10-02','food',408.00,1),(6,'2025-10-02','travel',562.00,1),(7,'2025-10-02','entertainment',187.00,1),(8,'2025-10-02','healthcare',267.00,1),(9,'2025-10-03','food',339.00,1),(10,'2025-10-03','travel',195.00,1),(11,'2025-10-03','entertainment',348.00,1),(12,'2025-10-03','healthcare',583.00,1),(13,'2025-10-04','food',185.00,1),(14,'2025-10-04','travel',258.00,1),(15,'2025-10-04','entertainment',422.00,1),(16,'2025-10-04','healthcare',577.00,1),(17,'2025-10-05','food',296.00,1),(18,'2025-10-05','travel',243.00,1),(19,'2025-10-05','entertainment',347.00,1),(20,'2025-10-05','healthcare',295.00,1),(21,'2025-10-06','food',163.00,1),(22,'2025-10-06','travel',368.00,1),(23,'2025-10-06','entertainment',389.00,1),(24,'2025-10-06','healthcare',67.00,1),(25,'2025-10-07','food',470.00,1),(26,'2025-10-07','travel',366.00,1),(27,'2025-10-07','entertainment',597.00,1),(28,'2025-10-07','healthcare',185.00,1),(29,'2025-10-08','food',507.00,1),(30,'2025-10-08','travel',179.00,1),(31,'2025-10-08','entertainment',589.00,1),(32,'2025-10-08','healthcare',324.00,1),(33,'2025-10-09','food',419.00,1),(34,'2025-10-09','travel',456.00,1),(35,'2025-10-09','entertainment',436.00,1),(36,'2025-10-09','healthcare',317.00,1),(37,'2025-10-10','food',194.00,1),(38,'2025-10-10','travel',62.00,1),(39,'2025-10-10','entertainment',163.00,1),(40,'2025-10-10','healthcare',132.00,1),(41,'2025-10-11','food',336.00,1),(42,'2025-10-11','travel',278.00,1),(43,'2025-10-11','entertainment',552.00,1),(44,'2025-10-11','healthcare',241.00,1),(45,'2025-10-12','food',487.00,1),(46,'2025-10-12','travel',449.00,1),(47,'2025-10-12','entertainment',307.00,1),(48,'2025-10-12','healthcare',324.00,1),(49,'2025-10-13','food',511.00,1),(50,'2025-10-13','travel',291.00,1),(51,'2025-10-13','entertainment',85.00,1),(52,'2025-10-13','healthcare',245.00,1),(53,'2025-10-14','food',453.00,1),(54,'2025-10-14','travel',180.00,1),(55,'2025-10-14','entertainment',98.00,1),(56,'2025-10-14','healthcare',133.00,1),(57,'2025-10-15','food',270.00,1),(58,'2025-10-15','travel',138.00,1),(59,'2025-10-15','entertainment',467.00,1),(60,'2025-10-15','healthcare',290.00,1),(61,'2025-10-16','food',420.00,1),(62,'2025-10-16','travel',240.00,1),(63,'2025-10-16','entertainment',284.00,1),(64,'2025-10-16','healthcare',579.00,1),(65,'2025-10-17','food',526.00,1),(66,'2025-10-17','travel',159.00,1),(67,'2025-10-17','entertainment',301.00,1),(68,'2025-10-17','healthcare',97.00,1),(69,'2025-10-18','food',529.00,1),(70,'2025-10-18','travel',109.00,1),(71,'2025-10-18','entertainment',184.00,1),(72,'2025-10-18','healthcare',277.00,1),(73,'2025-10-19','food',180.00,1),(74,'2025-10-19','travel',466.00,1),(75,'2025-10-19','entertainment',265.00,1),(76,'2025-10-19','healthcare',346.00,1),(77,'2025-10-20','food',297.00,1),(78,'2025-10-20','travel',88.00,1),(79,'2025-10-20','entertainment',463.00,1),(80,'2025-10-20','healthcare',135.00,1),(81,'2025-10-21','food',273.00,1),(82,'2025-10-21','travel',329.00,1),(83,'2025-10-21','entertainment',187.00,1),(84,'2025-10-21','healthcare',287.00,1),(85,'2025-10-22','food',364.00,1),(86,'2025-10-22','travel',393.00,1),(87,'2025-10-22','entertainment',533.00,1),(88,'2025-10-22','healthcare',97.00,1),(89,'2025-10-23','food',381.00,1),(90,'2025-10-23','travel',412.00,1),(91,'2025-10-23','entertainment',444.00,1),(92,'2025-10-23','healthcare',170.00,1),(93,'2025-10-24','food',194.00,1),(94,'2025-10-24','travel',469.00,1),(95,'2025-10-24','entertainment',467.00,1),(96,'2025-10-24','healthcare',405.00,1),(97,'2025-10-25','food',589.00,1),(98,'2025-10-25','travel',310.00,1),(99,'2025-10-25','entertainment',333.00,1),(100,'2025-10-25','healthcare',234.00,1),(101,'2025-10-26','food',426.00,1),(102,'2025-10-26','travel',419.00,1),(103,'2025-10-26','entertainment',50.00,1),(104,'2025-10-26','healthcare',137.00,1),(105,'2025-10-27','food',534.00,1),(106,'2025-10-27','travel',500.00,1),(107,'2025-10-27','entertainment',568.00,1),(108,'2025-10-27','healthcare',509.00,1),(109,'2025-10-28','food',163.00,1),(110,'2025-10-28','travel',571.00,1),(111,'2025-10-28','entertainment',122.00,1),(112,'2025-10-28','healthcare',365.00,1),(113,'2025-10-29','food',482.00,1),(114,'2025-10-29','travel',573.00,1),(115,'2025-10-29','entertainment',164.00,1),(116,'2025-10-29','healthcare',123.00,1),(117,'2025-10-30','food',225.00,1),(118,'2025-10-30','travel',348.00,1),(119,'2025-10-30','entertainment',191.00,1),(120,'2025-10-30','healthcare',402.00,1),(121,'2025-10-31','food',297.00,1),(122,'2025-10-31','travel',132.00,1),(123,'2025-10-31','entertainment',495.00,1),(124,'2025-10-31','healthcare',114.00,1),(125,'2025-11-01','food',216.00,1),(126,'2025-11-01','travel',284.00,1),(127,'2025-11-01','entertainment',169.00,1),(128,'2025-11-01','healthcare',274.00,1),(129,'2025-11-02','food',151.00,1),(130,'2025-11-02','travel',385.00,1),(131,'2025-11-02','entertainment',243.00,1),(132,'2025-11-02','healthcare',484.00,1),(133,'2025-11-03','food',420.00,1),(134,'2025-11-03','travel',267.00,1),(135,'2025-11-03','entertainment',184.00,1),(136,'2025-11-03','healthcare',116.00,1),(137,'2025-11-04','food',124.00,1),(138,'2025-11-04','travel',174.00,1),(139,'2025-11-04','entertainment',224.00,1),(140,'2025-11-04','healthcare',453.00,1),(141,'2025-11-05','food',361.00,1),(142,'2025-11-05','travel',194.00,1),(143,'2025-11-05','entertainment',210.00,1),(144,'2025-11-05','healthcare',366.00,1),(145,'2025-11-06','food',317.00,1),(146,'2025-11-06','travel',355.00,1),(147,'2025-11-06','entertainment',386.00,1),(148,'2025-11-06','healthcare',53.00,1),(149,'2025-11-07','food',591.00,1),(150,'2025-11-07','travel',88.00,1),(151,'2025-11-07','entertainment',552.00,1),(152,'2025-11-07','healthcare',413.00,1),(153,'2025-11-02','travel',400.00,1);
/*!40000 ALTER TABLE `expenses` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-17 19:50:05
