-- MySQL dump 10.13  Distrib 8.0.12, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: web
-- ------------------------------------------------------
-- Server version	8.0.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `hackers`
--

DROP TABLE IF EXISTS `hackers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `hackers` (
  `idhackers` int(11) NOT NULL,
  `handle` varchar(45) DEFAULT NULL,
  `about` longtext,
  `avatar` varchar(45) DEFAULT NULL,
  `realname` mediumtext,
  PRIMARY KEY (`idhackers`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hackers`
--

LOCK TABLES `hackers` WRITE;
/*!40000 ALTER TABLE `hackers` DISABLE KEYS */;
INSERT INTO `hackers` VALUES (1,'W17CH3R','Enjoys long walks on the beach with your mom.','aa.png','Felicia Diggs'),(2,'BL4Z3R','First computer was a Commodore 64.  Current computer is an E-Machine.','ab.png','James Cox'),(3,'D14BL0','Ready for Satanism to go mainstream','ac.png','Orlando Washington'),(4,'PR1M4 D0NN4','Can make a flashlight out of nothing but a tube of toothpaste, 3 feet of duct tape, and a flashlight.','ad.png','John Hinson'),(5,'V3RM1N','Bathed once.  It was awful.','ae.png','Robert Stern'),(6,'DUCKL1N6','Still thinks MySpace is coming back.','af.png','Rosa Schiro');
/*!40000 ALTER TABLE `hackers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hackhistory`
--

DROP TABLE IF EXISTS `hackhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `hackhistory` (
  `idwebdata` int(11) NOT NULL,
  `target` varchar(45) DEFAULT NULL,
  `description` longtext,
  `hacker` varchar(45) DEFAULT NULL,
  `loot` longtext,
  PRIMARY KEY (`idwebdata`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hackhistory`
--

LOCK TABLES `hackhistory` WRITE;
/*!40000 ALTER TABLE `hackhistory` DISABLE KEYS */;
INSERT INTO `hackhistory` VALUES (1,'NSA','No hack necessary.  They\'re leaky AF.','DUCKL1N6','Some sweet tools'),(2,'BMW','Permanently disable the turn-signal function on vehicles produced during presence on network.','PR1M4 D0NN4','Bragging Rights - Chaos'),(3,'Valve','Stole Half-Life 3 source code','PR1M4 D0NN4','Dumped full product database - got release date of Half-Life 3'),(4,'Santa Clause','Blind SQL injections resuled in discovering current Naught/Nice list as well as admin rights to modify','6H0UL','Added Tom Hanks to naughty list.  Chaos will follow.');
/*!40000 ALTER TABLE `hackhistory` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-10-02 14:15:23
