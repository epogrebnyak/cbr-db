-- MySQL dump 10.13  Distrib 5.6.16, for Win32 (x86)
--
-- Host: localhost    Database: cbr_db
-- ------------------------------------------------------
-- Server version	5.6.16

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
-- Table structure for table `alloc`
--

DROP TABLE IF EXISTS `alloc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alloc` (
  `line` int(11) DEFAULT NULL,
  `conto` int(11) DEFAULT NULL,
  `mult` decimal(32,0) DEFAULT NULL,
  `la_p` double DEFAULT NULL,
  `lev` int(1) NOT NULL DEFAULT '0',
  `step` int(1) NOT NULL DEFAULT '0',
  `is_extra` int(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `alloc_raw`
--

DROP TABLE IF EXISTS `alloc_raw`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alloc_raw` (
  `line` int(10) DEFAULT NULL,
  `conto` int(10) DEFAULT NULL,
  `mult` int(10) DEFAULT NULL,
  `src` char(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `balance`
--

DROP TABLE IF EXISTS `balance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `balance` (
  `dt` date DEFAULT NULL,
  `line` int(11) DEFAULT NULL,
  `lev` int(1) NOT NULL DEFAULT '0',
  `la_p` double DEFAULT NULL,
  `regn` smallint(6) DEFAULT NULL,
  `has_iv` tinyint(4) DEFAULT NULL,
  `ir` decimal(65,0) DEFAULT NULL,
  `iv` decimal(65,0) DEFAULT NULL,
  `itogo` decimal(65,0) DEFAULT NULL,
  KEY `bal_index_1` (`line`,`regn`,`dt`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `balance_line_name`
--

DROP TABLE IF EXISTS `balance_line_name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `balance_line_name` (
  `dot_id` varchar(10) DEFAULT NULL,
  `txt` varchar(256) DEFAULT NULL,
  `line` int(10) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `balance_test_items`
--

DROP TABLE IF EXISTS `balance_test_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `balance_test_items` (
  `dt` date DEFAULT NULL,
  `line` int(11) DEFAULT NULL,
  `regn` smallint(6) DEFAULT NULL,
  `itogo` decimal(65,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `balance_uniform`
--

DROP TABLE IF EXISTS `balance_uniform`;
/*!50001 DROP VIEW IF EXISTS `balance_uniform`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `balance_uniform` (
  `line` tinyint NOT NULL,
  `lev` tinyint NOT NULL,
  `regn` tinyint NOT NULL,
  `dt` tinyint NOT NULL,
  `itogo` tinyint NOT NULL,
  `ir` tinyint NOT NULL,
  `iv` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `bank`
--

DROP TABLE IF EXISTS `bank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bank` (
  `regn` int(11) NOT NULL,
  `regn_name` varchar(445) CHARACTER SET utf8 DEFAULT NULL,
  UNIQUE KEY `1` (`regn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `f101`
--

DROP TABLE IF EXISTS `f101`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `f101` (
  `dt` date NOT NULL,
  `regn` smallint(6) NOT NULL,
  `conto` mediumint(9) NOT NULL,
  `a_p` tinyint(4) DEFAULT NULL,
  `ir` bigint(20) DEFAULT NULL,
  `iv` bigint(20) DEFAULT NULL,
  `itogo` bigint(20) NOT NULL,
  `has_iv` tinyint(4) DEFAULT NULL,
  `conto_3` mediumint(9) DEFAULT NULL,
  PRIMARY KEY (`dt`,`regn`,`conto`,`itogo`),
  KEY `i_conto` (`conto`),
  KEY `i_regn` (`regn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `f102`
--
DROP TABLE IF EXISTS `f102`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `f102` (
  `dt` date,
  `regn` int(11),
  `quart` int(1),
  `year` int(11),
  `code` varchar(10),
  `ir` bigint(20),
  `iv` bigint(20),
  `itogo` bigint(20),
  `has_iv` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`regn`, `quart`, `year`, `code`, `itogo`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `list_alloc_line_all`
--

DROP TABLE IF EXISTS `list_alloc_line_all`;
/*!50001 DROP VIEW IF EXISTS `list_alloc_line_all`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `list_alloc_line_all` (
  `line` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `list_bank_names`
--

DROP TABLE IF EXISTS `list_bank_names`;
/*!50001 DROP VIEW IF EXISTS `list_bank_names`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `list_bank_names` (
  `regn` tinyint NOT NULL,
  `regn_name` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `list_conto_all`
--

DROP TABLE IF EXISTS `list_conto_all`;
/*!50001 DROP VIEW IF EXISTS `list_conto_all`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `list_conto_all` (
  `conto` tinyint NOT NULL,
  `a_p` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `list_date_all`
--

DROP TABLE IF EXISTS `list_date_all`;
/*!50001 DROP VIEW IF EXISTS `list_date_all`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `list_date_all` (
  `dt` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `list_regn_all`
--

DROP TABLE IF EXISTS `list_regn_all`;
/*!50001 DROP VIEW IF EXISTS `list_regn_all`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `list_regn_all` (
  `regn` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `major_bank`
--

DROP TABLE IF EXISTS `major_bank`;
/*!50001 DROP VIEW IF EXISTS `major_bank`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `major_bank` (
  `regn` tinyint NOT NULL,
  `regn_name` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `plan`
--

DROP TABLE IF EXISTS `plan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `plan` (
  `plan` char(1) DEFAULT NULL,
  `conto` varchar(5) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  KEY `plan_unique` (`conto`,`plan`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sprav102`
--

DROP TABLE IF EXISTS `sprav102`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sprav102` (
  `nom` int(11) NOT NULL,
  `prstr` int(11) DEFAULT NULL,
  `code` varchar(10) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`nom`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `temp_alloc_line`
--

DROP TABLE IF EXISTS `temp_alloc_line`;
/*!50001 DROP VIEW IF EXISTS `temp_alloc_line`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `temp_alloc_line` (
  `line` tinyint NOT NULL,
  `dot_id` tinyint NOT NULL,
  `txt` tinyint NOT NULL,
  `lev` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `temp_alloc_not_listed`
--

DROP TABLE IF EXISTS `temp_alloc_not_listed`;
/*!50001 DROP VIEW IF EXISTS `temp_alloc_not_listed`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `temp_alloc_not_listed` (
  `ac` tinyint NOT NULL,
  `conto` tinyint NOT NULL,
  `a_p` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `temp_tail`
--

DROP TABLE IF EXISTS `temp_tail`;
/*!50001 DROP VIEW IF EXISTS `temp_tail`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `temp_tail` (
  `dt` tinyint NOT NULL,
  `line` tinyint NOT NULL,
  `lev` tinyint NOT NULL,
  `la_p` tinyint NOT NULL,
  `regn` tinyint NOT NULL,
  `ir` tinyint NOT NULL,
  `iv` tinyint NOT NULL,
  `itogo` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `temp_vtb`
--

DROP TABLE IF EXISTS `temp_vtb`;
/*!50001 DROP VIEW IF EXISTS `temp_vtb`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `temp_vtb` (
  `line` tinyint NOT NULL,
  `txt` tinyint NOT NULL,
  `regn` tinyint NOT NULL,
  `dt` tinyint NOT NULL,
  `ir` tinyint NOT NULL,
  `iv` tinyint NOT NULL,
  `itogo` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `test_alloc_not_in_f101`
--

DROP TABLE IF EXISTS `test_alloc_not_in_f101`;
/*!50001 DROP VIEW IF EXISTS `test_alloc_not_in_f101`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `test_alloc_not_in_f101` (
  `ac` tinyint NOT NULL,
  `conto` tinyint NOT NULL,
  `a_p` tinyint NOT NULL,
  `line` tinyint NOT NULL,
  `mult` tinyint NOT NULL,
  `d` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `test_alloc_not_listed`
--

DROP TABLE IF EXISTS `test_alloc_not_listed`;
/*!50001 DROP VIEW IF EXISTS `test_alloc_not_listed`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `test_alloc_not_listed` (
  `ac` tinyint NOT NULL,
  `conto` tinyint NOT NULL,
  `a_p` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `test_balance_residual`
--

DROP TABLE IF EXISTS `test_balance_residual`;
/*!50001 DROP VIEW IF EXISTS `test_balance_residual`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `test_balance_residual` (
  `dt` tinyint NOT NULL,
  `regn` tinyint NOT NULL,
  `ap1` tinyint NOT NULL,
  `ap2` tinyint NOT NULL,
  `diff` tinyint NOT NULL,
  `diff_p` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `test_f101_duplicates`
--

DROP TABLE IF EXISTS `test_f101_duplicates`;
/*!50001 DROP VIEW IF EXISTS `test_f101_duplicates`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `test_f101_duplicates` (
  `regn` tinyint NOT NULL,
  `dt` tinyint NOT NULL,
  `conto` tinyint NOT NULL,
  `c` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `test_f101_residual`
--

DROP TABLE IF EXISTS `test_f101_residual`;
/*!50001 DROP VIEW IF EXISTS `test_f101_residual`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `test_f101_residual` (
  `dt` tinyint NOT NULL,
  `regn` tinyint NOT NULL,
  `ap1` tinyint NOT NULL,
  `ap2` tinyint NOT NULL,
  `diff` tinyint NOT NULL,
  `diff_p` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `test_negative_199`
--

DROP TABLE IF EXISTS `test_negative_199`;
/*!50001 DROP VIEW IF EXISTS `test_negative_199`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `test_negative_199` (
  `dt` tinyint NOT NULL,
  `line` tinyint NOT NULL,
  `lev` tinyint NOT NULL,
  `la_p` tinyint NOT NULL,
  `regn` tinyint NOT NULL,
  `ir` tinyint NOT NULL,
  `iv` tinyint NOT NULL,
  `itogo` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `test_ref_items`
--

DROP TABLE IF EXISTS `test_ref_items`;
/*!50001 DROP VIEW IF EXISTS `test_ref_items`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `test_ref_items` (
  `dt` tinyint NOT NULL,
  `regn` tinyint NOT NULL,
  `ref_div_fact` tinyint NOT NULL,
  `ref` tinyint NOT NULL,
  `fact` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `tmp_balance_view`
--

DROP TABLE IF EXISTS `tmp_balance_view`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tmp_balance_view` (
  `line` int(11) DEFAULT NULL,
  `lev` int(1) DEFAULT NULL,
  `regn` int(11) DEFAULT NULL,
  `dt` date DEFAULT NULL,
  `itogo` decimal(65,0) NOT NULL DEFAULT '0',
  `ir` decimal(65,0) NOT NULL DEFAULT '0',
  `iv` decimal(65,0) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tmp_dt_view`
--

DROP TABLE IF EXISTS `tmp_dt_view`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tmp_dt_view` (
  `cpart` varchar(5) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `regn` varchar(4) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `line` varchar(4) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `dt_group_1` mediumtext CHARACTER SET utf8
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tmp_output_ir`
--

DROP TABLE IF EXISTS `tmp_output_ir`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tmp_output_ir` (
  `cpart` varchar(5) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `regn` varchar(11) CHARACTER SET utf8 DEFAULT NULL,
  `line` varchar(11) CHARACTER SET utf8 DEFAULT NULL,
  `dt_group_1` longtext CHARACTER SET utf8
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tmp_output_itogo`
--

DROP TABLE IF EXISTS `tmp_output_itogo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tmp_output_itogo` (
  `cpart` varchar(5) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `regn` varchar(11) CHARACTER SET utf8 DEFAULT NULL,
  `line` varchar(11) CHARACTER SET utf8 DEFAULT NULL,
  `dt_group_1` longtext CHARACTER SET utf8
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tmp_output_iv`
--

DROP TABLE IF EXISTS `tmp_output_iv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tmp_output_iv` (
  `cpart` varchar(5) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `regn` varchar(11) CHARACTER SET utf8 DEFAULT NULL,
  `line` varchar(11) CHARACTER SET utf8 DEFAULT NULL,
  `dt_group_1` longtext CHARACTER SET utf8
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'cbr_db3'
--
/*!50003 DROP PROCEDURE IF EXISTS `alloc_make` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `alloc_make`()
BEGIN






DROP TABLE IF EXISTS prealloc;

create table prealloc as
Select line, conto, sum(mult) mult, left(line,1) * 1 as la_p, 0 lev, 1 step, 0 is_extra  from 
(	
	select a.line, l.conto, a.mult, "derived form level-one accounts" as src from alloc_raw a
		inner join (select distinct conto, conto_3 from f101) l
		on a.conto = l.conto_3
	   where a.conto < 1000
	UNION ALL
	select line, conto, mult, "actual level-two accounts" src from alloc_raw a
		where a.conto > 1000
) s	
group by line, conto
order by 1,2;



UPDATE prealloc SET lev = 10, step = 3 where right(line, 3) = "000";
UPDATE prealloc SET lev = 20, step = 3 where right(line, 2) =  "00" AND mid(line, 4, 1) != "0";
UPDATE prealloc SET lev = 30, step = 3 where right(line, 1) =   "0" AND mid(line, 5, 1) != "0";
UPDATE prealloc SET lev = 40, step = 3 where right(line, 1) !=  "0";

insert prealloc 
Select left(a.line,3)*1000 + 900 line, a.conto, a.mult, a.la_p, 20 lev, 41 step, 1 is_extra  from 
 (select distinct left(b.line,3)*1000 line from  prealloc b where b.lev = 20) k
 left join prealloc a on k.line = a.line 
 left join (select line, conto, lev, mult from prealloc p where p.lev = 20) m 
 on (a.conto = m.conto and left(a.line,3) = left(m.line,3)) 
 where m.line is NULL;
insert prealloc 
Select left(a.line,4)*100 + 90 line, a.conto, a.mult, a.la_p, 30 lev, 42 step, 1 is_extra  from 
 (select distinct left(b.line,4)*100 line from  prealloc b where b.lev = 30) k
 left join prealloc a on k.line = a.line
 left join (select line, conto, lev, mult from prealloc p where p.lev = 30) m 
 on (a.conto = m.conto and left(a.line,4) = left(m.line,4)) 
 where m.line is NULL;

delete from prealloc where mult = 0 and is_extra = 1;
delete from prealloc where mult = 0 and is_extra = 0;

delete from alloc;
DROP TABLE IF EXISTS alloc;

create Table alloc as Select * from prealloc;




DROP TABLE prealloc;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `alloc_make_insert_not_listed` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `alloc_make_insert_not_listed`()
BEGIN

drop table if exists account_not_listed;
create temporary table account_not_listed as
select line, conto, mult, "not listed in alloc" src from (
select a.conto ac, f.conto conto, f.a_p, (CASE WHEN f.a_p = 1 THEN 199000 ELSE 299000 END) line, 1 mult 
from prealloc a right join list_conto_all f ON a.conto = f.conto 
where f.conto != 0 
Having ac is Null) z;

insert prealloc 
select line, conto, mult, left(line,1) * 1 as la_p, 0 lev, 2 step, 1 is_extra 
from account_not_listed;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `balance_make` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `balance_make`()
BEGIN



call balance_make_step_1();
call balance_make_saldo_198_298();
call balance_make_insert_totals();




END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `balance_make_group` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `balance_make_group`()
BEGIN


drop table if exists balance_group;
create temporary table if not exists balance_group 
as select * from balance limit 0; 

insert into balance_group
select dt, line, lev, la_p, -1 regn, sum(ir), sum(iv), sum(itogo) from  balance 
where regn in (
  1481	
,  354	   
, 1000	
, 1623	
, 2748	
, 3349	
) 
group by balance.dt, balance.line, balance.regn;


insert into balance_group
select dt, line, lev, la_p, -3 regn, sum(ir), sum(iv), sum(itogo) from  balance 
where regn in (
  354	   
, 1000	
, 1623	
, 2748	
, 3349	
)
group by dt, line, balance.regn;


insert into balance_group
select dt, line, lev, la_p, -1000 regn, sum(ir), sum(iv), sum(itogo) from  balance 
where regn in (
 1000	
, 1623	
, 2748	
) group by dt, line, balance.regn;


insert into balance_group
select dt, line, lev, la_p, -964 regn, sum(ir), sum(iv), sum(itogo) from  balance 
where regn in (
  1470	
, 1942	
, 2790	
, 3340	
)
group by dt, line, balance.regn;

insert into balance 
select * from balance_group;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `balance_make_insert_totals` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `balance_make_insert_totals`()
BEGIN

drop table if exists tmp_balance_total;
create table tmp_balance_total as
select dt, 100000 line, 1 lev, 1 la_p, regn, has_iv, sum(ir) ir, sum(iv) iv, sum(itogo) itogo from balance
where la_p = 1 and line != 100000 and lev = 10
group by regn, dt;

insert into tmp_balance_total
select dt, 200000 line, 1 lev, 2 la_p, regn, has_iv, sum(ir) ir, sum(iv) iv, sum(itogo) itogo from balance
where la_p = 2 and line != 200000 and lev = 10
group by regn, dt;

drop table if exists balance_net;
create temporary table balance_net as
select b.dt, 500 line, 1 lev, 0 la_p, b.regn, b.has_iv, (b.ir - z.ir) ir, 
                                            (b.iv - z.iv) iv, 
														  (b.itogo-z.itogo) as itogo 
from tmp_balance_total b 
left join tmp_balance_total z on b.dt = z.dt and b.regn = z.regn 
where b.line = 100000 and z.line = 200000 
group by dt, regn;

insert into balance
select * from tmp_balance_total;

insert into balance
select * from   balance_net;

drop table tmp_balance_total;
drop table balance_net;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `balance_make_saldo_198_298` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`test_user`@`localhost` PROCEDURE `balance_make_saldo_198_298`()
BEGIN











drop table if exists saldo_198_298;







create temporary table saldo_198_298 as















select 



   a.dt, a.line, a.lev, a.la_p, a.regn, a.has_iv,



   case when (a.ir > b.ir) then (a.ir - b.ir) else 0 end ir,



	case when (a.iv > b.iv) then (a.iv - b.iv) else 0 end iv,



   



	case when (a.ir > b.ir) then (a.ir - b.ir) else 0 end



 +	case when (a.iv > b.iv) then (a.iv - b.iv) else 0 end  itogo	



from balance a



left join balance b 



on a.dt = b.dt and a.regn = b.regn 



where a.line = 198000 



and b.line = 298000 







group by a.dt, a.line, a.lev, a.la_p, a.regn







UNION ALL















select 



   b.dt, b.line, b.lev, b.la_p, b.regn, b.has_iv,



	case when (a.ir < b.ir) then (- a.ir + b.ir) else 0 end ir, 



	case when (a.iv < b.iv) then (- a.iv + b.iv) else 0 end iv, 



   



	case when (a.ir < b.ir) then (- a.ir + b.ir) else 0 end  



 + case when (a.iv < b.iv) then (- a.iv + b.iv) else 0 end itogo 



	from balance a



left join balance b 



on a.dt = b.dt and a.regn = b.regn 



where a.line = 198000 



and b.line = 298000











group by b.dt, b.line, b.lev, b.la_p, b.regn;











delete from balance where line = 198000;



delete from balance where line = 298000;







insert into balance



select * from saldo_198_298;







END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `balance_make_step_1` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `balance_make_step_1`()
BEGIN

drop table if exists balance;



create table if not exists balance as 
SELECT  dt, line, 
        lev, la_p,
        regn,
        has_iv,
        sum(   ir*mult) ir,
        sum(   iv*mult) iv,
        sum(itogo*mult) itogo
from alloc a left join f101 v on v.conto = a.conto
where v.conto Is not null
group by dt, line, regn;

create index bal_index_1 on balance (line, regn, dt);

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `balance_report_1` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `balance_report_1`()
BEGIN

call balance_report_line_dt_3tables;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `balance_report_line_dt_3tables` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `balance_report_line_dt_3tables`()
BEGIN



set session group_concat_max_len=100000;













DROP  TABLE IF EXISTS tmp_balance_view;

CREATE  TABLE tmp_balance_view AS

SELECT * from balance_uniform;





DROP  TABLE IF EXISTS tmp_dt_view;

CREATE  TABLE IF NOT EXISTS tmp_dt_view AS

	SELECT 'cpart' as cpart,

    	'regn' as regn,

    	'line' as line,

		group_concat(d.dt order by d.dt asc separator '\t') as dt_group_1

		FROM 

		(select distinct dt from balance_uniform) d;

		





DROP  TABLE IF EXISTS tmp_output_itogo;

CREATE  TABLE tmp_output_itogo AS

Select * from tmp_dt_view

UNION ALL

SELECT * FROM (

	   SELECT 'itogo' as cpart, regn, line,  

		group_concat(coalesce(itogo, '') order by dt asc separator '\t') as itogo

	   FROM tmp_balance_view

	   Where regn is not Null

		GROUP BY regn, line

		ORDER BY regn, line) g_1



;





DROP  TABLE IF EXISTS tmp_output_ir;

CREATE  TABLE tmp_output_ir AS

Select * from tmp_dt_view

UNION ALL

SELECT * FROM (

	   SELECT 'ir' as cpart, regn, line,  

		group_concat(coalesce(ir, '') order by dt asc separator '\t') as itogo

	   FROM tmp_balance_view

	   Where regn is not Null

		GROUP BY regn, line

		ORDER BY regn, line) g_2



;





DROP  TABLE IF EXISTS tmp_output_iv;

CREATE  TABLE tmp_output_iv AS

Select * from tmp_dt_view

UNION ALL

SELECT * FROM (

	   SELECT 'iv' as cpart, regn, line,  

		group_concat(coalesce(iv, '') order by dt asc separator '\t') as itogo

	   FROM tmp_balance_view

	   Where regn is not Null

		GROUP BY regn, line

		ORDER BY regn, line) g_3



;
















END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `balance_report_run` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `balance_report_run`()
BEGIN



set session group_concat_max_len=100000;





CALL temp_balance_report_line_dt(1481);





CALL temp_balance_report_line_dt(354);





CALL temp_balance_report_line_dt(1000);





CALL temp_balance_report_line_dt(3349);





CALL temp_balance_report_line_dt(1942);





CALL temp_balance_report_line_dt(1470);









END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `make_file` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `make_file`(IN `sql_line` VARCHAR(50), IN `file_prefix` VARCHAR(50))
BEGIN



SET @sql_text = CONCAT (sql_line

		 ,	" into outfile '"

       , "D:\\\\databases\\\\dump\\\\"       

       , DATE_FORMAT( NOW(), '%Y%m%d')

       , '_' 

		 ,  CONVERT(ROUND(curtime()/100+0,0), CHAR)       

       , '_' 

		 , file_prefix 

       , ".txt'"

		 , " CHARACTER SET utf8 

  FIELDS TERMINATED BY '\\t'

  ESCAPED BY ''

  LINES TERMINATED BY '\\r\\n'");

       

PREPARE s1 FROM @sql_text;

EXECUTE s1;

DROP PREPARE s1;



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `make_view` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `make_view`(IN `view_name` CHAR(50))
BEGIN

call make_file(CONCAT("select * from ", view_name), view_name);

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `temp_abandoned_balance_make_saldo_198_298` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `temp_abandoned_balance_make_saldo_198_298`()
BEGIN



drop table if exists saldo_198_298;



create temporary table saldo_198_298 as







select 

   a.dt, a.line, a.lev, a.la_p, a.regn, a.has_iv,

   case when (a.ir > b.ir) then (a.ir - b.ir) else 0 end ir,

	case when (a.iv > b.iv) then (a.iv - b.iv) else 0 end iv,

   

	case when (a.ir > b.ir) then (a.ir - b.ir) else 0 end

 +	case when (a.iv > b.iv) then (a.iv - b.iv) else 0 end  itogo	

from balance a

left join balance b 

on a.dt = b.dt and a.regn = b.regn 

where a.line = 198000 

and b.line = 298000 

and a.has_iv = 1



group by a.dt, a.line, a.lev, a.la_p, a.regn



UNION ALL







select 

   b.dt, b.line, b.lev, b.la_p, b.regn, b.has_iv,

	case when (a.ir < b.ir) then (- a.ir + b.ir) else 0 end ir, 

	case when (a.iv < b.iv) then (- a.iv + b.iv) else 0 end iv, 

   

	case when (a.ir < b.ir) then (- a.ir + b.ir) else 0 end  

 + case when (a.iv < b.iv) then (- a.iv + b.iv) else 0 end itogo 

	from balance a

left join balance b 

on a.dt = b.dt and a.regn = b.regn 

where a.line = 198000 

and b.line = 298000

and a.has_iv = 1



group by b.dt, b.line, b.lev, b.la_p, b.regn







UNION ALL

select 

   a.dt, a.line, a.lev, a.la_p, a.regn, b.has_iv, 0 ir, 0 iv,    

   case when (a.itogo > b.itogo) then (a.itogo - b.itogo) else 0 end itogo      

from balance a left join balance b 

on a.dt = b.dt and a.regn = b.regn 

where a.line = 198000 and b.line = 298000 

and a.has_iv = 0

group by a.dt, a.line, a.lev, a.la_p, a.regn



UNION ALL

select 

   b.dt, b.line, b.lev, b.la_p, b.regn, b.has_iv,  0 ir, 0 iv, 

   case when (a.itogo < b.itogo) then (- a.itogo + b.itogo) else 0 end itogo     

	from balance a left join balance b 

on a.dt = b.dt and a.regn = b.regn 

where a.line = 198000 and b.line = 298000

and a.has_iv = 0



group by b.dt, b.line, b.lev, b.la_p, b.regn;





delete from balance where line = 198000;

delete from balance where line = 298000;



insert into balance

select * from saldo_198_298;



END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `temp_balance_report_line_dt` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `temp_balance_report_line_dt`(IN `p_regn` INT)
BEGIN




DROP TEMPORARY TABLE IF EXISTS tmp_balance_view;
CREATE TEMPORARY TABLE tmp_balance_view AS

SELECT
	h.line,

	d.dt,  
   IFNULL(b.itogo,0) as itogo,
   IFNULL(b.iv,0) as iv,
   IFNULL(b.ir,0) as ir
FROM (select distinct line from alloc) h 
LEFT JOIN 
	(select distinct dt from f101) d ON TRUE
LEFT JOIN 
	(select * from balance where regn = p_regn) as b
		ON  b.line = h.line 
		AND b.dt = d.dt
GROUP BY
	h.line, 
	d.dt;


DROP TEMPORARY TABLE IF EXISTS tmp_dt_view;
CREATE TEMPORARY TABLE tmp_dt_view AS
	SELECT 0 as _line,
	   
		group_concat(d.dt order by d.dt asc separator '\t') as dt1,
		'' e1,
		group_concat(d.dt order by d.dt asc separator '\t') as dt2,
		'' e2,
		group_concat(d.dt order by d.dt asc separator '\t') as dt3 
		FROM 
		(select distinct dt from f101) d;


DROP TEMPORARY TABLE IF EXISTS tmp_output_view;
CREATE TEMPORARY TABLE tmp_output_view AS
  SELECT * from tmp_dt_view
UNION ALL
    SELECT * FROM (
    SELECT line, 
    
	group_concat(coalesce(itogo, '') order by dt asc separator '\t') as itogo, 
	'' e1,
	group_concat(coalesce(ir, '') order by dt asc separator '\t') as ir, 
	'' e2,
	group_concat(coalesce(iv, '') order by dt asc separator '\t') as iv	
	FROM tmp_balance_view
	GROUP BY line
	ORDER BY line) g
UNION	ALL
   Select '  Регистрационный номер:' line, p_regn, '', '', '', ''
UNION
   Select '  Название организации:' line,  regn_name, '', '', '', '' from bank where regn = p_regn
Order by 1
;

call make_file('SELECT * FROM tmp_output_view', CONCAT('balance_', p_regn));

SELECT * FROM tmp_output_view;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `temp_empty_all_tables` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `temp_empty_all_tables`()
BEGIN
delete from bank;
delete from f101;
delete from f102;
delete from plan;
delete from sprav102;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `temp_wipe_non_major` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `temp_wipe_non_major`()
delete from f101 
where regn not in (
  1481	
, 354	   

, 1000	
, 1623	
, 2748	

, 3349	
, 1326	

, 1470	
, 1942	
, 2790	
, 3340	
) ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `temp_work_calls` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `temp_work_calls`()
BEGIN


select distinct code from 
(select code, sim_r, sim_v, itogo, itogo-sim_v-sim_r as zero from f102 having zero  > 100) a;

call make_file("select * from list_bank_names", "names");

update alloc_raw 
set line = 199000, mult = mult  * -1
where line = 299000;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `test_balance_make` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `test_balance_make`()
BEGIN

select "Test must return 4 empty sets below" as msg;

call balance_make_step_1;
select * from test_balance_residual;



call balance_make_saldo_198_298();
select * from test_balance_residual limit 10;

call balance_make_insert_totals;
select * from test_balance_residual limit 10;

select * from balance where line = 500 and itogo !=0; 




END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `test_count_line_numbers` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `test_count_line_numbers`()
BEGIN
select dt, regn, count(*) from balance_uniform
group by dt, regn;

select dt, regn, count(*) from balance
group by dt, regn; 

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `test_netting` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `test_netting`()
BEGIN

select "Netting example - must have at least one zero per line" as msg;

select * from balance where line in (198000, 298000) and regn = 1326 and
dt in ("2013-12-01", "2013-01-01") order by dt;


select * from saldo_198_298 where line in (198000, 298000) and regn = 1326 and
dt in ("2013-12-01", "2013-01-01") order by dt;

END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Final view structure for view `balance_uniform`
--

/*!50001 DROP TABLE IF EXISTS `balance_uniform`*/;
/*!50001 DROP VIEW IF EXISTS `balance_uniform`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `balance_uniform` AS select `a`.`line` AS `line`,`b`.`lev` AS `lev`,`m`.`regn` AS `regn`,`d`.`dt` AS `dt`,ifnull(`b`.`itogo`,0) AS `itogo`,ifnull(`b`.`ir`,0) AS `ir`,ifnull(`b`.`iv`,0) AS `iv` from (((`list_alloc_line_all` `a` left join `major_bank` `m` on(1)) left join `list_date_all` `d` on(1)) left join `balance` `b` on(((`a`.`line` = `b`.`line`) and (`m`.`regn` = `b`.`regn`) and (`d`.`dt` = `b`.`dt`)))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `list_alloc_line_all`
--

/*!50001 DROP TABLE IF EXISTS `list_alloc_line_all`*/;
/*!50001 DROP VIEW IF EXISTS `list_alloc_line_all`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `list_alloc_line_all` AS select distinct `balance`.`line` AS `line` from `balance` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `list_bank_names`
--

/*!50001 DROP TABLE IF EXISTS `list_bank_names`*/;
/*!50001 DROP VIEW IF EXISTS `list_bank_names`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `list_bank_names` AS select `l`.`regn` AS `regn`,`b`.`regn_name` AS `regn_name` from (`list_regn_all` `l` left join `bank` `b` on((`l`.`regn` = `b`.`regn`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `list_conto_all`
--

/*!50001 DROP TABLE IF EXISTS `list_conto_all`*/;
/*!50001 DROP VIEW IF EXISTS `list_conto_all`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `list_conto_all` AS select distinct `f101`.`conto` AS `conto`,`f101`.`a_p` AS `a_p` from `f101` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `list_date_all`
--

/*!50001 DROP TABLE IF EXISTS `list_date_all`*/;
/*!50001 DROP VIEW IF EXISTS `list_date_all`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `list_date_all` AS select distinct `f101`.`dt` AS `dt` from `f101` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `list_regn_all`
--

/*!50001 DROP TABLE IF EXISTS `list_regn_all`*/;
/*!50001 DROP VIEW IF EXISTS `list_regn_all`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `list_regn_all` AS select distinct `f101`.`regn` AS `regn` from `f101` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `major_bank`
--

/*!50001 DROP TABLE IF EXISTS `major_bank`*/;
/*!50001 DROP VIEW IF EXISTS `major_bank`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `major_bank` AS select `bank`.`regn` AS `regn`,`bank`.`regn_name` AS `regn_name` from `bank` where (`bank`.`regn` in (1481,354,964,1000,1623,2748,3349,1326,1470,1942,2790,3340)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `temp_alloc_line`
--

/*!50001 DROP TABLE IF EXISTS `temp_alloc_line`*/;
/*!50001 DROP VIEW IF EXISTS `temp_alloc_line`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `temp_alloc_line` AS select `a`.`line` AS `line`,ifnull(`b`.`dot_id`,'') AS `dot_id`,ifnull(`b`.`txt`,'') AS `txt`,`a`.`lev` AS `lev` from (`alloc` `a` left join `balance_line_name` `b` on((`a`.`line` = `b`.`line`))) group by `a`.`line`,`b`.`dot_id`,`b`.`txt` order by `a`.`line` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `temp_alloc_not_listed`
--

/*!50001 DROP TABLE IF EXISTS `temp_alloc_not_listed`*/;
/*!50001 DROP VIEW IF EXISTS `temp_alloc_not_listed`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `temp_alloc_not_listed` AS select `a`.`conto` AS `ac`,`f`.`conto` AS `conto`,`f`.`a_p` AS `a_p` from (`list_conto_all` `f` left join `alloc` `a` on((`a`.`conto` = `f`.`conto`))) where ((`f`.`conto` <> 0) and (`a`.`conto` < 80000)) having isnull(`ac`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `temp_tail`
--

/*!50001 DROP TABLE IF EXISTS `temp_tail`*/;
/*!50001 DROP VIEW IF EXISTS `temp_tail`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `temp_tail` AS select `balance`.`dt` AS `dt`,`balance`.`line` AS `line`,`balance`.`lev` AS `lev`,`balance`.`la_p` AS `la_p`,`balance`.`regn` AS `regn`,`balance`.`ir` AS `ir`,`balance`.`iv` AS `iv`,`balance`.`itogo` AS `itogo` from `balance` where ((`balance`.`line` in (198000,298000)) and (`balance`.`regn` = 3349) and (`balance`.`dt` in ('2013-12-01','2013-01-01'))) order by `balance`.`dt` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `temp_vtb`
--

/*!50001 DROP TABLE IF EXISTS `temp_vtb`*/;
/*!50001 DROP VIEW IF EXISTS `temp_vtb`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `temp_vtb` AS select `b`.`line` AS `line`,`n`.`txt` AS `txt`,`b`.`regn` AS `regn`,`b`.`dt` AS `dt`,`b`.`ir` AS `ir`,`b`.`iv` AS `iv`,`b`.`itogo` AS `itogo` from (`balance_uniform` `b` left join `balance_line_name` `n` on((`b`.`line` = `n`.`line`))) where ((`b`.`regn` = 1000) and ((`b`.`lev` = 10) or (`b`.`lev` = 0)) and (`b`.`dt` = '2014-11-01')) order by `b`.`line` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `test_alloc_not_in_f101`
--

/*!50001 DROP TABLE IF EXISTS `test_alloc_not_in_f101`*/;
/*!50001 DROP VIEW IF EXISTS `test_alloc_not_in_f101`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `test_alloc_not_in_f101` AS select `a`.`conto` AS `ac`,`f`.`conto` AS `conto`,`f`.`a_p` AS `a_p`,(case when (`f`.`a_p` = 1) then 199000 else 299000 end) AS `line`,1 AS `mult`,`p`.`name` AS `d` from ((`list_conto_all` `f` left join `alloc` `a` on((`a`.`conto` = `f`.`conto`))) left join `plan` `p` on((`p`.`conto` = `f`.`conto`))) where ((`f`.`conto` <> 0) and (`f`.`conto` < 80000)) having isnull(`ac`) order by 3,2 */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `test_alloc_not_listed`
--

/*!50001 DROP TABLE IF EXISTS `test_alloc_not_listed`*/;
/*!50001 DROP VIEW IF EXISTS `test_alloc_not_listed`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `test_alloc_not_listed` AS select `a`.`conto` AS `ac`,`f`.`conto` AS `conto`,`f`.`a_p` AS `a_p` from (`list_conto_all` `f` left join `alloc` `a` on((`a`.`conto` = `f`.`conto`))) where ((`f`.`conto` <> 0) and (`a`.`conto` < 80000)) having isnull(`ac`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `test_balance_residual`
--

/*!50001 DROP TABLE IF EXISTS `test_balance_residual`*/;
/*!50001 DROP VIEW IF EXISTS `test_balance_residual`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `test_balance_residual` AS select `f`.`dt` AS `dt`,`f`.`regn` AS `regn`,sum((case when (`f`.`la_p` = 1) then `f`.`itogo` else 0 end)) AS `ap1`,sum((case when (`f`.`la_p` = 2) then `f`.`itogo` else 0 end)) AS `ap2`,(sum((case when (`f`.`la_p` = 1) then `f`.`itogo` else 0 end)) - sum((case when (`f`.`la_p` = 2) then `f`.`itogo` else 0 end))) AS `diff`,round((((sum((case when (`f`.`la_p` = 1) then `f`.`itogo` else 0 end)) / sum((case when (`f`.`la_p` = 2) then `f`.`itogo` else 0 end))) - 1) * 100),2) AS `diff_p` from (`major_bank` `m` left join `balance` `f` on((`m`.`regn` = `f`.`regn`))) where (`f`.`lev` = 10) group by `f`.`dt`,`f`.`regn` having (`diff` <> 0) order by 1,2 */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `test_f101_duplicates`
--

/*!50001 DROP TABLE IF EXISTS `test_f101_duplicates`*/;
/*!50001 DROP VIEW IF EXISTS `test_f101_duplicates`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `test_f101_duplicates` AS select `f101`.`regn` AS `regn`,`f101`.`dt` AS `dt`,`f101`.`conto` AS `conto`,count(0) AS `c` from `f101` group by `f101`.`regn`,`f101`.`dt`,`f101`.`conto` having (`c` <> 1) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `test_f101_residual`
--

/*!50001 DROP TABLE IF EXISTS `test_f101_residual`*/;
/*!50001 DROP VIEW IF EXISTS `test_f101_residual`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `test_f101_residual` AS select `f`.`dt` AS `dt`,`f`.`regn` AS `regn`,sum((case when (`f`.`a_p` = 1) then `f`.`itogo` else 0 end)) AS `ap1`,sum((case when (`f`.`a_p` = 2) then `f`.`itogo` else 0 end)) AS `ap2`,(sum((case when (`f`.`a_p` = 1) then `f`.`itogo` else 0 end)) - sum((case when (`f`.`a_p` = 2) then `f`.`itogo` else 0 end))) AS `diff`,round((abs(((sum((case when (`f`.`a_p` = 1) then `f`.`itogo` else 0 end)) / sum((case when (`f`.`a_p` = 2) then `f`.`itogo` else 0 end))) - 1)) * pow(10,9)),2) AS `diff_p` from `f101` `f` where (`f`.`conto` < 80000) group by `f`.`dt`,`f`.`regn` having (`diff` <> 0) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `test_negative_199`
--

/*!50001 DROP TABLE IF EXISTS `test_negative_199`*/;
/*!50001 DROP VIEW IF EXISTS `test_negative_199`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `test_negative_199` AS select `balance`.`dt` AS `dt`,`balance`.`line` AS `line`,`balance`.`lev` AS `lev`,`balance`.`la_p` AS `la_p`,`balance`.`regn` AS `regn`,`balance`.`ir` AS `ir`,`balance`.`iv` AS `iv`,`balance`.`itogo` AS `itogo` from `balance` where ((`balance`.`line` = 199000) and ((`balance`.`itogo` < 0) or (`balance`.`ir` < 0) or (`balance`.`iv` < 0))) order by `balance`.`regn` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `test_ref_items`
--

/*!50001 DROP TABLE IF EXISTS `test_ref_items`*/;
/*!50001 DROP VIEW IF EXISTS `test_ref_items`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`test_user`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `test_ref_items` AS select `ba`.`dt` AS `dt`,`ba`.`regn` AS `regn`,((`ba`.`itogo` / `bb`.`itogo`) - 1) AS `ref_div_fact`,`ba`.`itogo` AS `ref`,`bb`.`itogo` AS `fact` from (`balance_test_items` `ba` left join `balance` `bb` on(((`ba`.`dt` = `bb`.`dt`) and (`ba`.`regn` = `bb`.`regn`) and (`ba`.`line` = `bb`.`line`)))) */;
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

-- Dump completed on 2015-06-24  3:48:13
