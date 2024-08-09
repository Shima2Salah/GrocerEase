-- Drop database
DROP DATABASE IF EXISTS ecommerce;

-- Create database + user if doesn't exist
CREATE DATABASE IF NOT EXISTS ecommerce;
CREATE USER IF NOT EXISTS 'ecomm_dev'@'localhost';
SET PASSWORD FOR 'ecomm_dev'@'localhost' = 'ecomm_dev_pwd';
GRANT ALL ON ecommerce.* TO 'ecomm_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'ecomm_dev'@'localhost';
FLUSH PRIVILEGES;

USE ecommerce;

-- Table structure for table categories

DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `name` VARCHAR(255) UNIQUE NOT NULL
);
-- Table structure for table products

DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `product_name` VARCHAR(255) NOT NULL,
    `price` DECIMAL(10, 2) NOT NULL,
    `description` VARCHAR(255),
    `image_url` VARCHAR(255),
    `category_id` INT NOT NULL,
    KEY `category_id` (`category_id`),
    CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES categories(`id`)
);
-- Table structure for table colors

DROP TABLE IF EXISTS `colors`;
CREATE TABLE `colors` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `color_name` VARCHAR(255) NOT NULL
);
-- Table structure for table products_colors

DROP TABLE IF EXISTS `products_colors`;
CREATE TABLE `products_colors` (
  `product_id` INT NOT NULL,
  `color_id` INT NOT NULL,
  PRIMARY KEY (`product_id`,`color_id`),
  KEY `color_id` (`color_id`),
  CONSTRAINT `product_color_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `product_color_ibfk_2` FOREIGN KEY (`color_id`) REFERENCES `colors` (`id`)
);
-- Table structure for table sizes

DROP TABLE IF EXISTS `sizes`;
CREATE TABLE `sizes` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `size_name` VARCHAR(255) NOT NULL
);
-- Table structure for table products_sizes

DROP TABLE IF EXISTS `products_sizes`;
CREATE TABLE `products_sizes` (
  `product_id` INT NOT NULL,
  `size_id` INT NOT NULL,
  PRIMARY KEY (`product_id`,`size_id`),
  KEY `size_id` (`size_id`),
  CONSTRAINT `product_size_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`),
  CONSTRAINT `product_size_ibfk_2` FOREIGN KEY (`size_id`) REFERENCES `sizes` (`id`)
);
-- Table structure for table users

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `first_name` VARCHAR(100) NOT NULL,
    `last_name` VARCHAR(100) NOT NULL,   
    `contact_number` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `password` VARCHAR(100) ,
    `country` VARCHAR(100) NOT NULL,
    `company_name` VARCHAR(100) NOT NULL,
    `address` VARCHAR(100) NOT NULL,
    `state_or_country` VARCHAR(100) NOT NULL,
    `postal_or_zip` VARCHAR(100) NOT NULL,
    `order_notes` VARCHAR(255)
);
-- Table structure for table orders

DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `user_id` INT NOT NULL,
    `total_price` DECIMAL(10, 2) NOT NULL,
    KEY `user_id` (`user_id`),
    CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES users(`id`)
);
-- Table structure for table order_items

DROP TABLE IF EXISTS `order_items`;
CREATE TABLE `order_items` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `order_id` INT NOT NULL,  
    `product_id` INT NOT NULL,
    `quantity` INT NOT NULL,
    `price` DECIMAL(10, 2) NOT NULL,
    KEY `order_id` (`order_id`),
    KEY `product_id` (`product_id`),
    CONSTRAINT `orders_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES order_items(`id`),
    CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES products(`id`)
);

-- Dummy data for categories table
INSERT INTO categories (name) VALUES
('Women'),
('Men'),
('Children');

-- Dummy data for products table
INSERT INTO products (product_name, price, description, image_url, category_id) VALUES
('Tank Top', 15.99, 'Sleeveless top for women', 'tank top.jpeg', 1),
('Corater', 29.99, 'Stylish corater for men', 'corater.jpeg', 2),
('Polo Shirt', 24.99, 'Classic polo shirt for children', 'Polo Shirt.jpeg', 3),
('Dress', 49.99, 'Elegant dress for women', 'Dress.jpeg', 1),
('Button-Up Shirt', 39.99, 'Formal shirt for men', 'button up shirt.jpeg', 2),
('Trousers', 34.99, 'Casual trousers for children', 'Trousers.jpeg', 3),
('Blouse', 29.99, 'Chic blouse for women', 'Blouse.jpeg', 1),
('Shorts', 19.99, 'Comfortable shorts for men', 'Shorts.jpeg', 2),
('Skirt', 39.99, 'Stylish skirt for children', 'Skirt.jpeg', 3);
-- Dummy data for colors table
INSERT INTO colors (color_name) VALUES
('Red'),
('Blue'),
('Green'),
('Purple'),
('White');

-- Dummy data for sizes table
INSERT INTO sizes (size_name) VALUES
('Small'),
('Medium'),
('Large'),
('Extra Large');

-- Dummy data for products_colors table
INSERT INTO products_colors (product_id, color_id) VALUES
(1, 1),
(2, 4),
(3, 5),
(4, 1),
(5, 4),
(6, 5),
(7, 1),
(8, 4),
(9, 5);

-- Dummy data for products_sizes table
INSERT INTO products_sizes (product_id, size_id) VALUES
(1, 2),
(2, 3),
(3, 4),
(4, 2),
(5, 3),
(6, 4),
(7, 2),
(8, 3),
(9, 4);

-- Dummy data for users table
INSERT INTO users (First_Name, Last_Name, contact_number, email, password, Country, Company_Name, Address, State_or_Country, Postal_or_Zip, Order_Notes) VALUES
('John', 'Doe', '123456789', 'john@example.com', 'password123', 'USA', 'ABC Inc.', '123 Main St', 'CA', '12345', 'N/A'),
('Jane', 'Smith', '987654321', 'jane@example.com', 'password456', 'Canada', 'XYZ Ltd.', '456 Maple Ave', 'ON', 'M1N2P3', 'Please deliver before 5 PM');

-- Dummy data for orders table
INSERT INTO orders (user_id, total_price) VALUES
(1, 689.92),
(2, 404.94);

-- Dummy data for order_items table
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 2, 31.98),
(1, 2, 1, 49.99),
(1, 3, 1, 29.99),
(1, 4, 1, 39.99),
(2, 1, 2, 59.98),
(2, 2, 1, 34.99),
(2, 3, 1, 19.99),
(2, 4, 1, 39.99);
