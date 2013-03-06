-- phpMyAdmin SQL Dump

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

DROP TABLE IF EXISTS `ingress_events`;
CREATE TABLE IF NOT EXISTS `ingress_events` (
  `guid` varchar(35) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT 'global event identifyer',
  `timestamp` datetime NOT NULL COMMENT 'date time of the event',
  `player_guid` varchar(35) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `portal_from_guid` varchar(35) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `portal_to_guid` varchar(35) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `event_plain_text` varchar(1024) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `event_action` int(11) NOT NULL,
  `event_type` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `event_team` varchar(30) COLLATE utf16_unicode_ci NOT NULL,
  `event_is_secured` int(11) NOT NULL,
  PRIMARY KEY (`guid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COLLATE=utf16_unicode_ci COMMENT='ingress event credentials';

DROP TABLE IF EXISTS `ingress_players`;
CREATE TABLE IF NOT EXISTS `ingress_players` (
  `guid` varchar(35) COLLATE utf8_unicode_ci NOT NULL COMMENT 'global user identifyer',
  `plain` varchar(30) COLLATE utf8_unicode_ci NOT NULL COMMENT 'user plain text nick name',
  `team` varchar(20) COLLATE utf8_unicode_ci NOT NULL COMMENT 'team name',
  `player_level` int(11) DEFAULT NULL,
  PRIMARY KEY (`guid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='ingress players credentials';

DROP TABLE IF EXISTS `ingress_portals`;
CREATE TABLE IF NOT EXISTS `ingress_portals` (
  `guid` varchar(35) COLLATE utf8_unicode_ci NOT NULL,
  `address` varchar(1024) COLLATE utf8_unicode_ci NOT NULL,
  `latE6` int(11) NOT NULL,
  `lngE6` int(11) NOT NULL,
  `name` varchar(300) COLLATE utf8_unicode_ci NOT NULL,
  `owner` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`guid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='ingress portals credentials';

DROP TABLE IF EXISTS `ingress_score`;
CREATE TABLE IF NOT EXISTS `ingress_score` (
  `score_date` datetime NOT NULL,
  `score_aliens` int(11) NOT NULL,
  `score_resistance` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COLLATE=utf16_unicode_ci;

DROP TABLE IF EXISTS `notification`;
CREATE TABLE IF NOT EXISTS `notification` (
  `guid` varchar(35) NOT NULL,
  `to_mail` tinyint(1) DEFAULT NULL,
  `to_jabber` tinyint(1) DEFAULT NULL,
  `to_user_id` int(11) NOT NULL,
  UNIQUE KEY `unq_idx_notif` (`guid`,`to_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `statistic`;
CREATE TABLE IF NOT EXISTS `statistic` (
  `player_guid` varchar(35) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `resonators_dep` int(11) NOT NULL DEFAULT '0',
  `resonators_des` int(11) NOT NULL DEFAULT '0',
  `links_dep` int(11) NOT NULL DEFAULT '0',
  `links_des` int(11) NOT NULL DEFAULT '0',
  `portal_cap` int(11) NOT NULL DEFAULT '0',
  `control_fld_dep` int(11) NOT NULL DEFAULT '0',
  `control_fld_des` int(11) NOT NULL DEFAULT '0',
  UNIQUE KEY `player_guid` (`player_guid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COLLATE=utf16_unicode_ci;

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_passwd` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ingress_user_guid` varchar(35) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_email` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_jabber` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `registration_code` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='users regidtered to the server' AUTO_INCREMENT=1 ;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
