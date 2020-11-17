-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Anamakine: localhost
-- Üretim Zamanı: 17 Kas 2020, 01:34:34
-- Sunucu sürümü: 10.4.14-MariaDB
-- PHP Sürümü: 7.4.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `personal`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`, `name`) VALUES
(1, 'oguz', '123', 'Oğuz Balkaya');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `articles`
--

CREATE TABLE `articles` (
  `id` int(11) NOT NULL,
  `subject` varchar(200) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `writenby` varchar(200) NOT NULL,
  `image` varchar(200) NOT NULL,
  `text` text NOT NULL,
  `status` enum('Published','Unpublished') NOT NULL DEFAULT 'Published'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `articles`
--

INSERT INTO `articles` (`id`, `subject`, `date`, `writenby`, `image`, `text`, `status`) VALUES
(22, 'İlk makale konusu', '2020-11-17 00:32:41', 'Oğuz Balkaya', '', 'İlk makale içeriği', 'Published');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `clubmemberships`
--

CREATE TABLE `clubmemberships` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `text` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `clubmemberships`
--

INSERT INTO `clubmemberships` (`id`, `name`, `text`) VALUES
(3, 'Kulüp adı', 'Kulüp açıklaması..');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `contactforms`
--

CREATE TABLE `contactforms` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `message` text NOT NULL,
  `date` varchar(100) NOT NULL,
  `status` enum('Answered','Waiting') NOT NULL DEFAULT 'Waiting'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `contactforms`
--

INSERT INTO `contactforms` (`id`, `name`, `email`, `message`, `date`, `status`) VALUES
(2, 'Oğuz Balkaya', 'oguz.balkaya@gmail.com', 'Deneme mesaj...', '2020-11-16 22:23:59.562102', 'Waiting');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `education`
--

CREATE TABLE `education` (
  `id` int(11) NOT NULL,
  `school` varchar(200) NOT NULL,
  `start` varchar(100) NOT NULL,
  `finish` varchar(100) NOT NULL,
  `text` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `education`
--

INSERT INTO `education` (`id`, `school`, `start`, `finish`, `text`) VALUES
(6, 'Çanakkale Onsekiz Mart Üniversitesi', '2017', 'Halen', '<p>Bilgisayar M&uuml;hendisliği&nbsp; -&nbsp; 3. sınıf</p>\r\n');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `subscribers`
--

CREATE TABLE `subscribers` (
  `id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `emailsha` varchar(100) NOT NULL,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `status` enum('Active','Inactive') NOT NULL DEFAULT 'Active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `subscribers`
--

INSERT INTO `subscribers` (`id`, `email`, `emailsha`, `date`, `status`) VALUES
(1, 'oguz.balkaya@gmail.com', 'oguz.balkaya@gmail.com', '2020-11-15 21:46:02', 'Active');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `talents`
--

CREATE TABLE `talents` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `text` text NOT NULL,
  `purcent` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `talents`
--

INSERT INTO `talents` (`id`, `name`, `text`, `purcent`) VALUES
(15, 'Yetenek', 'Yetenek açıklaması', 20);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `workexperiences`
--

CREATE TABLE `workexperiences` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `start` varchar(100) NOT NULL,
  `finish` varchar(100) NOT NULL,
  `text` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `workexperiences`
--

INSERT INTO `workexperiences` (`id`, `name`, `start`, `finish`, `text`) VALUES
(3, 'İş adı', 'Temmuz 2020', 'Ağustos 2020', 'iş açıklaması');

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `clubmemberships`
--
ALTER TABLE `clubmemberships`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `contactforms`
--
ALTER TABLE `contactforms`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `education`
--
ALTER TABLE `education`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `subscribers`
--
ALTER TABLE `subscribers`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `talents`
--
ALTER TABLE `talents`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `workexperiences`
--
ALTER TABLE `workexperiences`
  ADD PRIMARY KEY (`id`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Tablo için AUTO_INCREMENT değeri `articles`
--
ALTER TABLE `articles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- Tablo için AUTO_INCREMENT değeri `clubmemberships`
--
ALTER TABLE `clubmemberships`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Tablo için AUTO_INCREMENT değeri `contactforms`
--
ALTER TABLE `contactforms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Tablo için AUTO_INCREMENT değeri `education`
--
ALTER TABLE `education`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Tablo için AUTO_INCREMENT değeri `subscribers`
--
ALTER TABLE `subscribers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Tablo için AUTO_INCREMENT değeri `talents`
--
ALTER TABLE `talents`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Tablo için AUTO_INCREMENT değeri `workexperiences`
--
ALTER TABLE `workexperiences`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
