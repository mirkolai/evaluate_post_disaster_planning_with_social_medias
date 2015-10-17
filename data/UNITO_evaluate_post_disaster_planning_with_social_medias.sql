-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tiempo de generación: 17-10-2015 a las 13:08:34
-- Versión del servidor: 5.5.44-0ubuntu0.14.04.1
-- Versión de PHP: 5.5.9-1ubuntu4.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de datos: `UNITO_evaluate_post_disaster_planning_with_social_medias`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tweet_genova`
--

CREATE TABLE IF NOT EXISTS `tweet_genova` (
  `id` bigint(20) NOT NULL,
  `text` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `admin_order_1` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `admin_order_2` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `admin_order_3` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date` datetime NOT NULL,
  `json` text COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tweet_geolocated`
--

CREATE TABLE IF NOT EXISTS `tweet_geolocated` (
  `id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `text` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `screen_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `RT` int(11) NOT NULL,
  `RP` int(11) NOT NULL,
  `place` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `json` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `comune` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `provincia` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `regione` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `provincia` (`provincia`),
  KEY `date` (`date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tweet_weather_phenomena`
--

CREATE TABLE IF NOT EXISTS `tweet_weather_phenomena` (
  `id` bigint(20) NOT NULL,
  `text` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `admin_order_1` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `admin_order_2` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `admin_order_3` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date` datetime NOT NULL,
  `json` text COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `twitter_places`
--

CREATE TABLE IF NOT EXISTS `twitter_places` (
  `id` varchar(50) NOT NULL,
  `json` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
