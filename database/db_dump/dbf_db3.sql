-- MySQL dump 10.13  Distrib 5.5.9, for Win32 (x86)
--
-- Host: localhost    Database: dbf_db3
-- ------------------------------------------------------
-- Server version	5.5.9-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bulk_f101_b`
--

DROP TABLE IF EXISTS `bulk_f101_b`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bulk_f101_b` (
  `dt` date NOT NULL DEFAULT '0000-00-00',
  `regn` smallint(6) NOT NULL DEFAULT '0',
  `num_sc` mediumint(9) NOT NULL DEFAULT '0',
  `a_p` tinyint(4) DEFAULT NULL,
  `itogo` bigint(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`dt`,`regn`,`num_sc`,`itogo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bulk_f101b1`
--

DROP TABLE IF EXISTS `bulk_f101b1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bulk_f101b1` (
  `dt` date NOT NULL DEFAULT '0000-00-00',
  `regn` smallint(6) NOT NULL DEFAULT '0',
  `num_sc` mediumint(9) NOT NULL DEFAULT '0',
  `a_p` tinyint(4) DEFAULT NULL,
  `ir` bigint(20) DEFAULT NULL,
  `iv` bigint(20) DEFAULT NULL,
  `itogo` bigint(20) NOT NULL DEFAULT '0',
  PRIMARY KEY (`dt`,`regn`,`num_sc`,`itogo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='DT	REGN	NUM_SC	A_P	IR	IV	IITG';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bulk_f101veb`
--

DROP TABLE IF EXISTS `bulk_f101veb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bulk_f101veb` (
  `conto` bigint(20) NOT NULL DEFAULT '0',
  `col2` bigint(20) DEFAULT NULL,
  `col3` bigint(20) DEFAULT NULL,
  `col4` bigint(20) DEFAULT NULL,
  `col5` bigint(20) DEFAULT NULL,
  `col6` bigint(20) DEFAULT NULL,
  `col7` bigint(20) DEFAULT NULL,
  `col8` bigint(20) DEFAULT NULL,
  `col9` bigint(20) DEFAULT NULL,
  `col10` bigint(20) DEFAULT NULL,
  `ir` bigint(20) DEFAULT NULL,
  `iv` bigint(20) DEFAULT NULL,
  `itogo` bigint(20) NOT NULL DEFAULT '0',
  `dt` date NOT NULL DEFAULT '0000-00-00',
  `a_p` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`conto`,`dt`,`itogo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bulk_f102_p`
--

DROP TABLE IF EXISTS `bulk_f102_p`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bulk_f102_p` (
  `regn` int(11) NOT NULL,
  `quart` int(1) NOT NULL,
  `year` int(11) NOT NULL,
  `code` varchar(10) NOT NULL,
  `itogo` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`regn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `bulk_f102_p`
--

DROP TABLE IF EXISTS `bulk_f102_p1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bulk_f102_p1` (
  `regn` int(11) NOT NULL,
  `quart` int(1) NOT NULL,
  `year` int(11) NOT NULL,
  `code` varchar(10) NOT NULL,
  `ir` bigint(20) DEFAULT NULL,
  `iv` bigint(20) DEFAULT NULL,
  `itogo` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`regn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cfg_date_in_focus`
--

DROP TABLE IF EXISTS `cfg_date_in_focus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cfg_date_in_focus` (
  `dt` date NOT NULL DEFAULT '0000-00-00'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cfg_date_limit`
--

DROP TABLE IF EXISTS `cfg_date_limit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cfg_date_limit` (
  `dt_start` date DEFAULT NULL,
  `dt_end` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cfg_regn_in_focus`
--

DROP TABLE IF EXISTS `cfg_regn_in_focus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cfg_regn_in_focus` (
  `regn` smallint(6) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `f101`
--

DROP TABLE IF EXISTS `f101`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `f101` (
  `dt` date NOT NULL DEFAULT '0000-00-00',
  `regn` smallint(6) NOT NULL DEFAULT '0',
  `conto` mediumint(9) NOT NULL DEFAULT '0',
  `a_p` tinyint(4) DEFAULT NULL,
  `ir` bigint(20) DEFAULT NULL,
  `iv` bigint(20) DEFAULT NULL,
  `itogo` bigint(20) NOT NULL DEFAULT '0',
  `has_iv` int(1) NOT NULL DEFAULT '0',
  `conto_3` decimal(9,0) DEFAULT NULL,
  PRIMARY KEY (`dt`,`regn`,`conto`,`itogo`),
  KEY `i_conto` (`conto`),
  KEY `i_regn` (`regn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `f101_long`
--

DROP TABLE IF EXISTS `f101_long`;
/*!50001 DROP VIEW IF EXISTS `f101_long`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `f101_long` (
  `dt` date,
  `regn` smallint(6),
  `conto` mediumint(9),
  `a_p` tinyint(4),
  `ir` bigint(20),
  `iv` bigint(20),
  `itogo` bigint(20),
  `has_iv` int(1),
  `conto_3` binary(0)
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `f101_part_f101_b`
--

DROP TABLE IF EXISTS `f101_part_f101_b`;
/*!50001 DROP VIEW IF EXISTS `f101_part_f101_b`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `f101_part_f101_b` (
  `dt` date,
  `regn` smallint(6),
  `conto` mediumint(9),
  `a_p` tinyint(4),
  `ir` int(1),
  `iv` int(1),
  `itogo` bigint(20),
  `has_iv` int(1),
  `conto_3` decimal(9,0)
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `f101_part_f101_private`
--

DROP TABLE IF EXISTS `f101_part_f101_private`;
/*!50001 DROP VIEW IF EXISTS `f101_part_f101_private`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `f101_part_f101_private` (
  `dt` date,
  `regn` int(3),
  `conto` bigint(20),
  `a_p` tinyint(4),
  `ir` bigint(20),
  `iv` bigint(20),
  `itogo` bigint(20),
  `has_iv` int(1),
  `conto_3` decimal(20,0)
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `f101_part_f101b1`
--

DROP TABLE IF EXISTS `f101_part_f101b1`;
/*!50001 DROP VIEW IF EXISTS `f101_part_f101b1`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `f101_part_f101b1` (
  `dt` date,
  `regn` smallint(6),
  `conto` mediumint(9),
  `a_p` tinyint(4),
  `ir` bigint(20),
  `iv` bigint(20),
  `itogo` bigint(20),
  `has_iv` int(1),
  `conto_3` decimal(9,0)
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `f101_small`
--

DROP TABLE IF EXISTS `f101_small`;
/*!50001 DROP VIEW IF EXISTS `f101_small`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `f101_small` (
  `dt` date,
  `regn` smallint(6),
  `conto` mediumint(9),
  `a_p` tinyint(4),
  `ir` int(1),
  `iv` int(1),
  `itogo` bigint(20),
  `has_iv` int(1),
  `conto_3` binary(0)
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `f101_veb`
--

DROP TABLE IF EXISTS `f101_veb`;
/*!50001 DROP VIEW IF EXISTS `f101_veb`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `f101_veb` (
  `dt` date,
  `regn` int(3),
  `conto` bigint(20),
  `a_p` tinyint(4),
  `ir` bigint(20),
  `iv` bigint(20),
  `itogo` bigint(20),
  `has_iv` int(1),
  `conto_3` binary(0)
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Dumping routines for database 'dbf_db3'
--
/*!50003 DROP PROCEDURE IF EXISTS `check_duplicates` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `check_duplicates`(IN `table_name` CHAR(50))
BEGIN

SET @prefix  = "SELECT dt, regn, conto, itogo, COUNT(*) cnt FROM ";
SET @postfix = " GROUP BY dt, regn, conto, itogo HAVING  cnt > 1;";
SET @sql_text = concat(@prefix, table_name, @postfix);

PREPARE s1 FROM @sql_text;
EXECUTE s1;
DROP PREPARE s1;

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `check_residuals` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `check_residuals`(IN `table_name` CHAR(50))
BEGIN

SET @prefix = "SELECT f.dt AS dt, f.regn AS regn, " 
" SUM(CASE WHEN (f.a_p = 1) THEN f.itogo ELSE 0 END) AS ap1,"
" SUM(CASE WHEN (f.a_p = 2) THEN f.itogo ELSE 0 END) AS ap2, "
" SUM(CASE WHEN (f.a_p = 1) THEN f.itogo ELSE 0 END) - " 
" SUM(CASE WHEN (f.a_p = 2) THEN f.itogo ELSE 0 END) AS diff FROM ";

SET @postfix = " f GROUP BY f.dt,f.regn HAVING diff != 0 order by diff";

SET @sql_text = concat(@prefix, table_name, @postfix);


PREPARE s1 FROM @sql_text;
EXECUTE s1;
DROP PREPARE s1;

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `f101_make_dataset` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`test_user`@`localhost`*/ /*!50003 PROCEDURE `f101_make_dataset`()
BEGIN



# call reset_table_f101;

drop table if exists f101;



# Note: this is the longest file for insert and running create speeds up the script

create table f101 as 

select dt, regn, conto, a_p,  ir,  iv, itogo, has_iv, conto_3 from f101_part_f101b1;



insert f101

select dt, regn, conto, a_p,  ir,  iv, itogo, has_iv, conto_3 from f101_part_f101_b;



insert f101

select dt, regn, conto, a_p,  ir,  iv, itogo, has_iv, conto_3 from f101_part_f101_private;





# add primary key and index

ALTER TABLE	f101 ADD PRIMARY KEY (`dt`, `regn`, `conto`, `itogo`);

ALTER TABLE	f101 ADD INDEX `i_conto` (`conto`);

ALTER TABLE	f101 ADD INDEX `i_regn` (`regn`);





END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_f101` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `insert_f101`()
BEGIN



call reset_table_f101;



delete from bulk_f101b1 where num_sc = 0;

delete from bulk_f101_b where num_sc = 0;



insert ignore f101

select dt, regn, conto, a_p,  ir,  iv, itogo, has_iv, conto_3 from f101_long

#where dt >= '2012-01-01'

;



insert ignore f101

select dt, regn, conto, a_p,  ir,  iv, itogo, has_iv, conto_3 from f101_small

#where dt >= '2012-01-01'

;



insert ignore f101

select dt, regn, conto, a_p,  ir,  iv, itogo, has_iv, conto_3 from f101_veb

#where dt >= '2012-01-01'

;



update f101 set conto_3 = round(conto/100,0);











END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `reset_db` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `reset_db`()
BEGIN

call reset_table_f101;
call reset_table_f101b1;
call reset_table_f101_b;
call reset_table_f101veb;

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `reset_table_f101` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `reset_table_f101`()
BEGIN

drop table f101;
CREATE TABLE f101 (
	`dt` DATE NOT NULL DEFAULT '0000-00-00',
	`regn` SMALLINT(6) NOT NULL DEFAULT '0',
	`conto` MEDIUMINT(9) NOT NULL DEFAULT '0',
	`a_p` TINYINT(4) NULL DEFAULT NULL,
	`ir` BIGINT(20) NULL DEFAULT NULL,
	`iv` BIGINT(20) NULL DEFAULT NULL,
	`itogo` BIGINT(20) NOT NULL DEFAULT '0',
	`has_iv` TINYINT(4) NULL DEFAULT NULL,
	`conto_3` MEDIUMINT(9) NULL DEFAULT NULL,
	PRIMARY KEY (`dt`, `regn`, `conto`, `itogo`),
	INDEX `i_conto` (`conto`),
	INDEX `i_regn` (`regn`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB;

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `reset_table_f101b1` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `reset_table_f101b1`()
BEGIN

DROP TABLE bulk_f101b1;
CREATE TABLE `bulk_f101b1` (
	`dt` DATE NOT NULL DEFAULT '0000-00-00',
	`regn` SMALLINT(6) NOT NULL DEFAULT '0',
	`num_sc` MEDIUMINT(9) NOT NULL DEFAULT '0',
	`a_p` TINYINT(4) NULL DEFAULT NULL,
	`ir` BIGINT(20) NULL DEFAULT NULL,
	`iv` BIGINT(20) NULL DEFAULT NULL,
	`itogo` BIGINT(20) NOT NULL DEFAULT '0',
	PRIMARY KEY (`dt`, `regn`, `num_sc`, `itogo`)
)
COMMENT='DT	REGN	NUM_SC	A_P	IR	IV	IITG'
COLLATE='utf8_general_ci'
ENGINE=InnoDB;



END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `reset_table_f101veb` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `reset_table_f101veb`()
BEGIN
delete from bulk_f101veb;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `reset_table_f101_b` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `reset_table_f101_b`()
BEGIN

drop table  bulk_f101_b;

CREATE TABLE bulk_f101_b (
	`dt` DATE NOT NULL DEFAULT '0000-00-00',
	`regn` SMALLINT(6) NOT NULL DEFAULT '0',
	`num_sc` MEDIUMINT(9) NOT NULL DEFAULT '0',
	`a_p` TINYINT(4) NULL DEFAULT NULL,
	`itogo` BIGINT(20) NOT NULL DEFAULT '0',
	PRIMARY KEY (`dt`, `regn`, `num_sc`, `itogo`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB;

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `temp_init_truncation_limits` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`test_user`@`localhost`*/ /*!50003 PROCEDURE `temp_init_truncation_limits`()
BEGIN



# cli input -> cfg_date_limit, cfg_regn_in_focus -> sql to obtain f101

# Risk: dates/regn relate only to form 101, msut include dates from form 102, other forms. 

# Risk: need to keep all regn somewhere



# this will be overwritten by command line user parameteres

create table if not exists cfg_date_limit as

select min(dt) dt_start, max(dt) dt_end from f101; 



# make a list of dates

select dt_start from cfg_date_limit INTO @start_date;

select dt_end from cfg_date_limit INTO @end_date;

# show to screen

# select @start_date, @end_date;



drop table if exists cfg_date_in_focus;

create table cfg_date_in_focus as

select distinct dt from bulk_f101b1 where dt >= @start_date and dt <= @end_date;





# this will be overwritten by command line user parameteres

create table if not exists cfg_regn_in_focus as

select distinct regn from bulk_f101b1

UNION ALL

select distinct regn from bulk_f101_b

UNION ALL

select distinct regn from bulk_f101veb; 



END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `test_f101_residual` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `test_f101_residual`()
BEGIN

SELECT f.dt AS dt,f.regn AS regn, SUM((CASE WHEN (f.a_p = 1) THEN f.itogo ELSE 0 END)) AS ap1, 

SUM((CASE WHEN (f.a_p = 2) THEN f.itogo ELSE 0 END)) AS ap2,

(SUM((CASE WHEN (f.a_p = 1) THEN f.itogo ELSE 0 END)) - SUM((CASE WHEN (f.a_p = 2) THEN f.itogo ELSE 0 END))) AS diff, 

ROUND((ABS(((SUM((CASE WHEN (f.a_p = 1) THEN f.itogo ELSE 0 END)) / 

SUM((CASE WHEN (f.a_p = 2) THEN f.itogo ELSE 0 END))) - 1)) * POW(10,9)),2) AS diff_p

FROM f101 f

WHERE (f.conto < 80000)

GROUP BY f.dt,f.regn

HAVING (diff <> 0);

END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `test_import` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_AUTO_VALUE_ON_ZERO' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50020 DEFINER=`root`@`localhost`*/ /*!50003 PROCEDURE `test_import`()
BEGIN



delete from bulk_f101b1 where num_sc = 0;
delete from bulk_f101_b where num_sc = 0;
CALL check_duplicates('f101_long');
CALL check_duplicates('f101_small');
CALL check_duplicates('f101_veb');
CALL check_residuals ('bulk_f101_B');
CALL check_residuals ('bulk_f101B1');
CALL check_residuals ('bulk_f101veb');


END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Final view structure for view `f101_long`
--

/*!50001 DROP TABLE IF EXISTS `f101_long`*/;
/*!50001 DROP VIEW IF EXISTS `f101_long`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `f101_long` AS select `bulk_f101b1`.`dt` AS `dt`,`bulk_f101b1`.`regn` AS `regn`,`bulk_f101b1`.`num_sc` AS `conto`,`bulk_f101b1`.`a_p` AS `a_p`,`bulk_f101b1`.`ir` AS `ir`,`bulk_f101b1`.`iv` AS `iv`,`bulk_f101b1`.`itogo` AS `itogo`,1 AS `has_iv`,NULL AS `conto_3` from `bulk_f101b1` where ((`bulk_f101b1`.`regn` in (1481,354,1000,1623,2748,3349,1326,1470,1942,2790,3340)) and (`bulk_f101b1`.`dt` >= '2012-01-01')) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `f101_part_f101_b`
--

/*!50001 DROP TABLE IF EXISTS `f101_part_f101_b`*/;
/*!50001 DROP VIEW IF EXISTS `f101_part_f101_b`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`test_user`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `f101_part_f101_b` AS select `d`.`dt` AS `dt`,`r`.`regn` AS `regn`,`sa`.`num_sc` AS `conto`,`sa`.`a_p` AS `a_p`,0 AS `ir`,0 AS `iv`,`sa`.`itogo` AS `itogo`,0 AS `has_iv`,round((`sa`.`num_sc` / 100),0) AS `conto_3` from ((`cfg_date_in_focus` `d` join `cfg_regn_in_focus` `r` on(1)) left join `bulk_f101_b` `sa` on(((`sa`.`dt` = `d`.`dt`) and (`r`.`regn` = `sa`.`regn`)))) where (`sa`.`num_sc` <> 0) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `f101_part_f101_private`
--

/*!50001 DROP TABLE IF EXISTS `f101_part_f101_private`*/;
/*!50001 DROP VIEW IF EXISTS `f101_part_f101_private`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`test_user`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `f101_part_f101_private` AS select `d`.`dt` AS `dt`,964 AS `regn`,`sa`.`conto` AS `conto`,`sa`.`a_p` AS `a_p`,`sa`.`ir` AS `ir`,`sa`.`iv` AS `iv`,`sa`.`itogo` AS `itogo`,1 AS `has_iv`,round((`sa`.`conto` / 100),0) AS `conto_3` from (`cfg_date_in_focus` `d` left join `bulk_f101veb` `sa` on((`sa`.`dt` = `d`.`dt`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `f101_part_f101b1`
--

/*!50001 DROP TABLE IF EXISTS `f101_part_f101b1`*/;
/*!50001 DROP VIEW IF EXISTS `f101_part_f101b1`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`test_user`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `f101_part_f101b1` AS select `d`.`dt` AS `dt`,`r`.`regn` AS `regn`,`sa`.`num_sc` AS `conto`,`sa`.`a_p` AS `a_p`,`sa`.`ir` AS `ir`,`sa`.`iv` AS `iv`,`sa`.`itogo` AS `itogo`,1 AS `has_iv`,round((`sa`.`num_sc` / 100),0) AS `conto_3` from ((`cfg_date_in_focus` `d` join `cfg_regn_in_focus` `r` on(1)) left join `bulk_f101b1` `sa` on(((`sa`.`dt` = `d`.`dt`) and (`r`.`regn` = `sa`.`regn`)))) where (`sa`.`num_sc` <> 0) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `f101_small`
--

/*!50001 DROP TABLE IF EXISTS `f101_small`*/;
/*!50001 DROP VIEW IF EXISTS `f101_small`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `f101_small` AS select `bulk_f101_b`.`dt` AS `dt`,`bulk_f101_b`.`regn` AS `regn`,`bulk_f101_b`.`num_sc` AS `conto`,`bulk_f101_b`.`a_p` AS `a_p`,0 AS `ir`,0 AS `iv`,`bulk_f101_b`.`itogo` AS `itogo`,0 AS `has_iv`,NULL AS `conto_3` from `bulk_f101_b` where ((`bulk_f101_b`.`regn` in (1481,354,1000,1623,2748,3349,1326,1470,1942,2790,3340)) and (`bulk_f101_b`.`dt` >= '2012-01-01')) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `f101_veb`
--

/*!50001 DROP TABLE IF EXISTS `f101_veb`*/;
/*!50001 DROP VIEW IF EXISTS `f101_veb`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `f101_veb` AS select `bulk_f101veb`.`dt` AS `dt`,964 AS `regn`,`bulk_f101veb`.`conto` AS `conto`,`bulk_f101veb`.`a_p` AS `a_p`,`bulk_f101veb`.`ir` AS `ir`,`bulk_f101veb`.`iv` AS `iv`,`bulk_f101veb`.`itogo` AS `itogo`,1 AS `has_iv`,NULL AS `conto_3` from `bulk_f101veb` where (`bulk_f101veb`.`dt` >= '2012-01-01') */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-06-23 16:23:09
