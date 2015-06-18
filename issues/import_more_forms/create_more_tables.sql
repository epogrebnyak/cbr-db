-- --------------------------------------------------------
-- Хост:                         localhost
-- Версия сервера:               5.5.9-log - MySQL Community Server (GPL)
-- ОС Сервера:                   Win32
-- HeidiSQL Версия:              8.3.0.4694
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Дамп структуры базы данных cbr_db
CREATE DATABASE IF NOT EXISTS `cbr_db` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `cbr_db`;


-- Дамп структуры для таблица cbr_db.bank
CREATE TABLE IF NOT EXISTS `bank` (
  `regn` int(11) NOT NULL,
  `regn_name` varchar(445) CHARACTER SET utf8 DEFAULT NULL,
  UNIQUE KEY `1` (`regn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Экспортируемые данные не выделены.


-- Дамп структуры для таблица cbr_db.f101
CREATE TABLE IF NOT EXISTS `f101` (
  `dt` date DEFAULT NULL,
  `regn` smallint(6) DEFAULT NULL,
  `conto` mediumint(9) DEFAULT NULL,
  `a_p` tinyint(4) DEFAULT NULL,
  `ir` bigint(20) DEFAULT NULL,
  `iv` bigint(20) DEFAULT NULL,
  `itogo` bigint(20) DEFAULT NULL,
  `has_iv` tinyint(4) DEFAULT NULL,
  `conto_3` mediumint(9) DEFAULT NULL,
  KEY `i_conto` (`conto`),
  KEY `i_regn` (`regn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Экспортируемые данные не выделены.


-- Дамп структуры для таблица cbr_db.f102
CREATE TABLE IF NOT EXISTS `f102` (
  `regn` int(11) NOT NULL,
  `quart` int(1) NOT NULL,
  `year` int(11) NOT NULL,
  `code` varchar(10) NOT NULL,
# adding these new fields
  `ir` bigint(20) DEFAULT NULL,
  `iv` bigint(20) DEFAULT NULL,
# end adding these new fields
  `itogo` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`year`,`quart`,`regn`,`code`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- Экспортируемые данные не выделены.


-- Дамп структуры для таблица cbr_db.plan
CREATE TABLE IF NOT EXISTS `plan` (
  `plan` char(1) DEFAULT NULL,
  `conto` varchar(5) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  UNIQUE KEY `plan_unique` (`conto`,`plan`),
  KEY `plan_key1` (`conto`,`plan`,`level`),
  KEY `plan_key2` (`level`,`conto`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- Экспортируемые данные не выделены.


-- Дамп структуры для таблица cbr_db.sprav102
CREATE TABLE IF NOT EXISTS `sprav102` (
  `nom` int(11) NOT NULL,
  `prstr` int(11) DEFAULT NULL,
  `code` varchar(10) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`nom`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- Экспортируемые данные не выделены.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
