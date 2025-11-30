-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 30, 2025 at 05:04 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `restaurante`
--

-- --------------------------------------------------------

--
-- Table structure for table `platos`
--

CREATE TABLE `platos` (
  `id` int(11) NOT NULL,
  `nombre` text NOT NULL,
  `precio` decimal(12,2) NOT NULL,
  `imagen` text DEFAULT NULL,
  `fecha_creacion` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `platos`
--

INSERT INTO `platos` (`id`, `nombre`, `precio`, `imagen`, `fecha_creacion`) VALUES
(1, 'Empanadas de Queso', 2.50, 'empanadas.jpg', '2025-11-03'),
(2, 'Sopa de Pollo', 3.75, 'sopa_pollo.jpg', '2025-10-15'),
(3, 'Filete de Res', 8.90, 'filete_res.jpg', '2025-09-28'),
(4, 'Pasta Alfredo', 7.20, 'pasta_alfredo.jpg', '2025-12-01'),
(5, 'Dulce de Chocolate', 4.50, 'dulce_chocolate.jpg', '2025-11-12'),
(6, 'Helado de Vainilla', 2.00, 'helado_vainilla.jpg', '2025-07-22'),
(7, 'Limonada Natural', 1.50, 'limonada.jpg', '2025-08-09'),
(8, 'Coca-Cola', 1.25, 'cocacola.jpg', '2025-10-02'),
(9, 'Ensalada César', 5.80, 'ensalada_cesar.jpg', '2025-09-13');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `platos`
--
ALTER TABLE `platos`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `platos`
--
ALTER TABLE `platos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
