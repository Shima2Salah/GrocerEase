-- Drop database
DROP DATABASE IF EXISTS grocerease;

-- Create database + user if doesn't exist
CREATE DATABASE IF NOT EXISTS grocerease;
CREATE USER IF NOT EXISTS 'grocer_dev'@'localhost';
SET PASSWORD FOR 'grocer_dev'@'localhost' = 'grocer_dev_pwd';
GRANT ALL ON grocerease.* TO 'grocer_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'grocer_dev'@'localhost';
FLUSH PRIVILEGES;

USE grocerease;


DROP TABLE IF EXISTS `admin_roles`;
CREATE TABLE `admin_roles` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `admin_role_name` VARCHAR(100) NOT NULL,
    `admin_role_description` VARCHAR(255)
);

DROP TABLE IF EXISTS `discounts`;
CREATE TABLE `discounts` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `discount_percentage` DECIMAL(10, 2) NOT NULL,
    `start_date` DATETIME NOT NULL,
    `end_date` DATETIME NOT NULL,
    `is_deleted` BOOLEAN DEFAULT FALSE,
    `deleted_at` DATETIME DEFAULT NULL
);

DROP TABLE IF EXISTS `coupons`;
CREATE TABLE `coupons` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `coupon_code` VARCHAR(100) UNIQUE NOT NULL,
    `amount` DECIMAL(10, 2) NOT NULL,
    `start_date` DATETIME NOT NULL,
    `end_date` DATETIME NOT NULL,
    `is_deleted` BOOLEAN DEFAULT FALSE,
    `deleted_at` DATETIME DEFAULT NULL
);

DROP TABLE IF EXISTS `payments`;
CREATE TABLE `payments` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `payment_method` VARCHAR(100) NOT NULL,
    `is_deleted` BOOLEAN DEFAULT FALSE,
    `deleted_at` DATETIME DEFAULT NULL
);

DROP TABLE IF EXISTS `orders_statuses`;
CREATE TABLE `orders_statuses` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `status_name` VARCHAR(100) NOT NULL,
    `is_deleted` BOOLEAN DEFAULT FALSE,
    `deleted_at` DATETIME DEFAULT NULL
);

DROP TABLE IF EXISTS `deliveries`;
CREATE TABLE `deliveries` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `delivery_name` VARCHAR(100) NOT NULL,
    `contact_number` VARCHAR(50) NOT NULL,
    `address` VARCHAR(100) NOT NULL,
    `is_active` INT NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `is_deleted` BOOLEAN DEFAULT FALSE,
    `deleted_at` DATETIME DEFAULT NULL
);

DROP TABLE IF EXISTS `admins`;
CREATE TABLE `admins` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `admin_name` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100) UNIQUE NOT NULL,
    `password_hash` VARCHAR(1024) NOT NULL,
    `admin_role_id` INT NOT NULL,
    `status` INT,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `is_deleted` BOOLEAN DEFAULT FALSE,
    `deleted_at` DATETIME DEFAULT NULL,
    KEY `admin_role_id` (`admin_role_id`),    
    CONSTRAINT `fk_admins_admin_role_id` FOREIGN KEY (`admin_role_id`) REFERENCES admin_roles(`id`)
);


DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `category_name` VARCHAR(255) UNIQUE NOT NULL,
    `created_by_admin_id` INT NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `is_deleted` BOOLEAN DEFAULT FALSE,
    `deleted_at` DATETIME DEFAULT NULL,
    KEY `created_by_admin_id` (`created_by_admin_id`),
    CONSTRAINT `fk_categories_created_by_admin_id` FOREIGN KEY (`created_by_admin_id`) REFERENCES admins(`id`)
);

DROP TABLE IF EXISTS `suppliers`;
CREATE TABLE `suppliers` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `supplier_name` VARCHAR(255) NOT NULL,
    `contact_number` VARCHAR(50) NOT NULL,
    `address` VARCHAR(100) NOT NULL,
    `created_by_admin_id` INT NOT NULL,
    `company_name` VARCHAR(255) NOT NULL,
    `email` VARCHAR(100) UNIQUE NOT NULL,
    `notes` VARCHAR(255),
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `is_deleted` BOOLEAN DEFAULT FALSE,
    `deleted_at` DATETIME DEFAULT NULL,
    KEY `created_by_admin_id` (`created_by_admin_id`),
    CONSTRAINT `fk_suppliers_created_by_admin_id` FOREIGN KEY (`created_by_admin_id`) REFERENCES admins(`id`)
);
DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `product_name` VARCHAR(255) NOT NULL,
    `unit_price` DECIMAL(10, 2),
    `image_url` VARCHAR(255),
    `description` VARCHAR(255),
    `supplier_id` INT NOT NULL,
    `created_by_admin_id` INT NOT NULL,
    `discount_id` INT,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `stock_weight` DECIMAL(10, 2),
    `weight` DECIMAL(10, 2),
    `category_id` INT NOT NULL,
    `is_deleted` BOOLEAN DEFAULT FALSE,
    `deleted_at` DATETIME DEFAULT NULL,
    KEY `category_id` (`category_id`),
    KEY `supplier_id` (`supplier_id`),
    KEY `created_by_admin_id` (`created_by_admin_id`),
    KEY `discount_id` (`discount_id`),
    CONSTRAINT `fk_products_category_id` FOREIGN KEY (`category_id`) REFERENCES categories(`id`),
    CONSTRAINT `fk_products_supplier_id` FOREIGN KEY (`supplier_id`) REFERENCES suppliers(`id`),
    CONSTRAINT `fk_products_created_by_admin_id` FOREIGN KEY (`created_by_admin_id`) REFERENCES admins(`id`),
    CONSTRAINT `fk_products_discount_id` FOREIGN KEY (`discount_id`) REFERENCES discounts(`id`)
);

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `first_name` VARCHAR(255) NOT NULL,
    `last_name` VARCHAR(255) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `contact_number` VARCHAR(50) NOT NULL,
    `country` VARCHAR(100) NOT NULL,
    `company_name` VARCHAR(100) NOT NULL,
    `address` VARCHAR(100) NOT NULL,
    `state_or_country` VARCHAR(100) NOT NULL,
    `postal_or_zip` VARCHAR(100) NOT NULL,
    `order_notes` VARCHAR(255),
    `password_hash` VARCHAR(100),
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `is_create_account` INT,
    `is_deleted` BOOLEAN DEFAULT FALSE,
    `deleted_at` DATETIME DEFAULT NULL
);

DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `total_price` DECIMAL(10, 2) NOT NULL,
    `delivery_id` INT,
    `order_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `status_id` INT NOT NULL DEFAULT 1,
    `payment_id` INT NOT NULL,
    `coupon_id` INT,
    `delivery_date` DATETIME,
    `payment_date` DATETIME,
    `payment_status` INT,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `is_deleted` BOOLEAN DEFAULT FALSE,
    `deleted_at` DATETIME DEFAULT NULL,
    KEY `user_id` (`user_id`),
    KEY `delivery_id` (`delivery_id`),
    KEY `status_id` (`status_id`),
    KEY `payment_id` (`payment_id`),
    KEY `coupon_id` (`coupon_id`),
    CONSTRAINT `fk_orders_user_id` FOREIGN KEY (`user_id`) REFERENCES users(`id`),
    CONSTRAINT `fk_orders_delivery_id` FOREIGN KEY (`delivery_id`) REFERENCES deliveries(`id`),
    CONSTRAINT `fk_orders_status_id` FOREIGN KEY (`status_id`) REFERENCES orders_statuses(`id`),
    CONSTRAINT `fk_orders_payment_id` FOREIGN KEY (`payment_id`) REFERENCES payments(`id`),
    CONSTRAINT `fk_orders_coupon_id` FOREIGN KEY (`coupon_id`) REFERENCES coupons(`id`)
);

DROP TABLE IF EXISTS `order_items`;
CREATE TABLE `order_items` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `product_id` INT NOT NULL,
    `amount` DECIMAL(10, 2) NOT NULL,
    `price` DECIMAL(10, 2) NOT NULL,
    `order_id` INT NOT NULL,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `is_deleted` BOOLEAN DEFAULT FALSE,
    `deleted_at` DATETIME DEFAULT NULL,
    KEY `order_id` (`order_id`),
    KEY `product_id` (`product_id`),
    CONSTRAINT `fk_order_items_product_id` FOREIGN KEY (`product_id`) REFERENCES products(`id`),
    CONSTRAINT `fk_order_items_order_id` FOREIGN KEY (`order_id`) REFERENCES orders(`id`)
);

-- Insert data into admin_roles table
INSERT INTO admin_roles (admin_role_name, admin_role_description) VALUES
('Super Admin', 'Has access to all administrative functions'),
('Product Manager', 'Manages product listings and categories'),
('Order Manager', 'Handles customer orders and deliveries');

-- Insert data into coupons table
INSERT INTO coupons (coupon_code, amount, start_date, end_date, is_deleted, deleted_at) VALUES
('WELCOME10', 10.00, '2024-08-01 00:00:00', '2024-12-31 23:59:59', FALSE, NULL),
('SUMMER15', 15.00, '2024-09-01 00:00:00', '2024-09-30 23:59:59', FALSE, NULL),
('FALL20', 20.00, '2024-10-01 00:00:00', '2024-10-31 23:59:59', FALSE, NULL);

-- Insert data into payments table
INSERT INTO payments (payment_method, is_deleted, deleted_at) VALUES
('Credit Card', FALSE, NULL),
('PayPal', FALSE, NULL),
('Cash on Delivery', FALSE, NULL);

-- Insert data into orders_statuses table
INSERT INTO orders_statuses (status_name, is_deleted, deleted_at) VALUES
('Pending', FALSE, NULL),
('Processing', FALSE, NULL),
('Shipped', FALSE, NULL),
('Delivered', FALSE, NULL),
('Cancelled', FALSE, NULL);

-- Insert data into deliveries table
INSERT INTO deliveries (delivery_name, contact_number, address, is_active, created_at, updated_at, is_deleted, deleted_at) VALUES
('Express Delivery', '123-456-7890', '123 Main St, City, Country', 1, NOW(), NOW(), FALSE, NULL),
('Standard Delivery', '098-765-4321', '456 Market St, City, Country', 1, NOW(), NOW(), FALSE, NULL);

-- Insert data into admins table
INSERT INTO admins (admin_name, email, password_hash, admin_role_id, status, created_at, updated_at, is_deleted, deleted_at) VALUES
('John Doe', 'john.doe@example.com', 'scrypt:32768:8:1$o1ZrINufvzvjYtSZ$b83c2094292cd85132cdd7eac55f5204f587ec5e4272b8685daa903c3149562b96b7c0ad5a9662d2c3daec7d0e0b5d0f69dd4cf55e1cbe68558fe8fec32e9501', 1, 1, NOW(), NOW(), FALSE, NULL),
('Jane Smith', 'jane.smith@example.com', 'hashed_password2', 2, 1, NOW(), NOW(), FALSE, NULL),
('Mark Johnson', 'mark.johnson@example.com', 'hashed_password3', 3, 1, NOW(), NOW(), FALSE, NULL);

-- Insert data into categories table
INSERT INTO categories (category_name, created_by_admin_id, created_at, updated_at, is_deleted, deleted_at) VALUES
('Bakery & Bread', 1, NOW(), NOW(), FALSE, NULL),
('Meat & Seafood', 2, NOW(), NOW(), FALSE, NULL),
('Frozen Foods', 1, NOW(), NOW(), FALSE, NULL),
('Snacks & Sweets', 1, NOW(), NOW(), FALSE, NULL),
('Beverages', 1, NOW(), NOW(), FALSE, NULL),
('Vegetables & Fruits', 2, NOW(), NOW(), FALSE, NULL);

-- Insert data into suppliers table
INSERT INTO suppliers (supplier_name, contact_number, address, created_by_admin_id, company_name, email, notes, created_at, updated_at, is_deleted, deleted_at) VALUES
('Fresh Farms', '123-456-7890', '123 Farm Lane', 1, 'Fresh Farms Co.', 'contact@freshfarms.com', 'Premium quality produce supplier', NOW(), NOW(), FALSE, NULL),
('Dairy Best', '234-567-8901', '456 Dairy Road', 2, 'Dairy Best Ltd.', 'contact@dairybest.com', 'Leading dairy products supplier', NOW(), NOW(), FALSE, NULL),
('Frozen Delight', '345-678-9012', '789 Frozen Blvd', 1, 'Frozen Delight Inc.', 'contact@frozendelight.com', 'Frozen foods supplier', NOW(), NOW(), FALSE, NULL),
('Sweet Snacks', '456-789-0123', '101 Sweet St', 2, 'Sweet Snacks Ltd.', 'contact@sweetsnacks.com', 'Snacks & sweets supplier', NOW(), NOW(), FALSE, NULL),
('Beverage World', '567-890-1234', '202 Beverage Ave', 2, 'Beverage World Co.', 'contact@beverageworld.com', 'Beverages supplier', NOW(), NOW(), FALSE, NULL),
('Green Harvest', '678-901-2345', '303 Green Way', 2, 'Green Harvest LLC', 'contact@greenharvest.com', 'Vegetables & fruits supplier', NOW(), NOW(), FALSE, NULL);

-- Insert data into products table
INSERT INTO products (product_name, unit_price, description, image_url, supplier_id, created_by_admin_id, discount_id, stock_weight, weight, category_id, created_at, updated_at, is_deleted, deleted_at) VALUES
('Whole Wheat Bread', 2.99, 'Freshly baked whole wheat bread', 'whole_wheat_bread.jpg', 1, 1, NULL, 50.00, 1.00, 1, NOW(), NOW(), FALSE, NULL),
('Croissants', 4.99, 'Flaky buttery croissants', 'croissants.jpg', 1, 1, NULL, 30.00, 0.50, 1, NOW(), NOW(), FALSE, NULL),
('Bagels', 3.49, 'Assorted bagels', 'bagels.jpg', 1, 1, NULL, 40.00, 1.00, 1, NOW(), NOW(), FALSE, NULL),
('Chicken Breast', 6.99, 'Boneless skinless chicken breast', 'chicken_breast.jpg', 2, 2, NULL, 100.00, 2.00, 2, NOW(), NOW(), FALSE, NULL),
('Salmon Fillets', 12.99, 'Fresh Atlantic salmon fillets', 'salmon_fillets.jpg', 2, 2, NULL, 50.00, 1.00, 2, NOW(), NOW(), FALSE, NULL),
('Ground Beef', 8.49, 'Lean ground beef', 'ground_beef.jpg', 2, 2, NULL, 80.00, 2.00, 2, NOW(), NOW(), FALSE, NULL),
('Frozen Pizza', 7.99, 'Pepperoni frozen pizza', 'frozen_pizza.jpg', 3, 1, NULL, 60.00, 1.50, 3, NOW(), NOW(), FALSE, NULL),
('Ice Cream', 4.49, 'Vanilla ice cream', 'ice_cream.jpg', 3, 1, NULL, 40.00, 1.00, 3, NOW(), NOW(), FALSE, NULL),
('Frozen Vegetables', 3.99, 'Mixed frozen vegetables', 'frozen_vegetables.jpg', 3, 1, NULL, 100.00, 2.00, 3, NOW(), NOW(), FALSE, NULL),
('Chocolate Bar', 1.99, 'Dark chocolate bar', 'chocolate_bar.jpg', 4, 3, NULL, 200.00, 0.10, 4, NOW(), NOW(), FALSE, NULL),
('Potato Chips', 2.49, 'Salted potato chips', 'potato_chips.jpg', 4, 3, NULL, 150.00, 0.20, 4, NOW(), NOW(), FALSE, NULL),
('Gummy Bears', 3.29, 'Fruit-flavored gummy bears', 'gummy_bears.jpg', 4, 3, NULL, 120.00, 0.25, 4, NOW(), NOW(), FALSE, NULL),
('Orange Juice', 4.99, 'Freshly squeezed orange juice', 'orange_juice.jpg', 5, 1, NULL, 60.00, 2.00, 5, NOW(), NOW(), FALSE, NULL),
('Cola', 1.29, 'Carbonated cola drink', 'cola.jpg', 5, 1, NULL, 100.00, 0.50, 5, NOW(), NOW(), FALSE, NULL),
('Bottled Water', 0.99, 'Spring bottled water', 'bottled_water.jpg', 5, 1, NULL, 500.00, 1.00, 5, NOW(), NOW(), FALSE, NULL),
('Lettuce', 1.79, 'Fresh iceberg lettuce', 'lettuce.jpg', 6, 2, NULL, 80.00, 1.00, 6, NOW(), NOW(), FALSE, NULL),
('Tomatoes', 2.49, 'Juicy red tomatoes', 'tomatoes.jpg', 6, 2, NULL, 120.00, 1.50, 6, NOW(), NOW(), FALSE, NULL),
('Bananas', 1.29, 'Bunch of ripe bananas', 'bananas.jpg', 6, 2, NULL, 200.00, 2.00, 6, NOW(), NOW(), FALSE, NULL),
('Broccoli', 2.49, 'Fresh organic broccoli', 'broccoli.jpg', 6, 2, NULL, 100.00, 1.00, 6, NOW(), NOW(), FALSE, NULL),
('Carrots', 1.99, 'Bag of fresh carrots', 'carrots.jpg', 6, 2, NULL, 200.00, 1.00, 6, NOW(), NOW(), FALSE, NULL),
('Spinach', 3.49, 'Fresh organic spinach leaves', 'spinach.jpg', 6, 2, NULL, 150.00, 0.75, 6, NOW(), NOW(), FALSE, NULL),
('Cucumbers', 1.99, 'Bag of fresh cucumber', 'cucumbers.jpg', 6, 2, NULL, 300.00, 0.50, 6, NOW(), NOW(), FALSE, NULL),
('Bell Peppers', 3.99, 'Mixed color bell peppers', 'bell_peppers.jpg', 6, 2, NULL, 120.00, 0.50, 6, NOW(), NOW(), FALSE, NULL),
('Potatoes', 2.79, 'Bag of fresh potatoes', 'potatoes.jpg', 6, 2, NULL, 300.00, 2.00, 6, NOW(), NOW(), FALSE, NULL),
('Apples', 4.99, 'Bag of fresh apples', 'apples.jpg', 6, 2, NULL, 100.00, 1.50, 6, NOW(), NOW(), FALSE, NULL),
('Oranges', 3.49, 'Fresh juicy oranges', 'oranges.jpg', 6, 2, NULL, 200.00, 2.00, 6, NOW(), NOW(), FALSE, NULL),
('Strawberries', 5.99, 'Box of fresh strawberries', 'strawberries.jpg', 6, 2, NULL, 100.00, 0.50, 6, NOW(), NOW(), FALSE, NULL),
('Blueberries', 4.99, 'Box of fresh blueberries', 'blueberries.jpg', 6, 2, NULL, 80.00, 0.50, 6, NOW(), NOW(), FALSE, NULL),
('Grapes', 3.99, 'Bag of seedless grapes', 'grapes.jpg', 6, 2, NULL, 120.00, 1.00, 6, NOW(), NOW(), FALSE, NULL);

-- Insert data into users table
INSERT INTO users (first_name, last_name, email, contact_number, country, company_name, address, state_or_country, postal_or_zip, order_notes, password_hash, created_at, updated_at, is_create_account, is_deleted, deleted_at) VALUES
('Alice', 'Johnson', 'alice.johnson@example.com', '111-222-3333', 'USA', 'Alice Corp', '789 Pine St', 'California', '90210', 'Please leave at the front door', 'hashed_password4', NOW(), NOW(), 1, FALSE, NULL),
('Bob', 'Williams', 'bob.williams@example.com', '222-333-4444', 'USA', 'Bob Enterprises', '123 Elm St', 'New York', '10001', 'Deliver after 5 PM', 'hashed_password5', NOW(), NOW(), 1, FALSE, NULL);

-- Insert data into orders table
INSERT INTO orders (user_id, total_price, delivery_id, order_date, status_id, payment_id, coupon_id, delivery_date, payment_date, payment_status, created_at, updated_at, is_deleted, deleted_at) VALUES
(1, 10.99, 1, NOW(), 2, 1, 1, NOW() + INTERVAL 3 DAY, NOW(), 1, NOW(), NOW(), FALSE, NULL),
(2, 15.99, 2, NOW(), 1, 2, 2, NOW() + INTERVAL 5 DAY, NOW(), 0, NOW(), NOW(), FALSE, NULL);

-- Insert data into order_items table
INSERT INTO order_items (product_id, amount, price, order_id, created_at, updated_at, is_deleted, deleted_at) VALUES
(1, 5.00, 9.95, 1, NOW(), NOW(), FALSE, NULL),
(3, 2.00, 5.00, 2, NOW(), NOW(), FALSE, NULL);
