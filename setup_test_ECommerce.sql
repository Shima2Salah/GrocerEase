-- prepares a  test SQL server for ecommerce

CREATE DATABASE IF NOT EXISTS ecommerce_test;
CREATE USER IF NOT EXISTS 'ecomm_test'@'localhost' IDENTIFIED BY 'ecomm_test_pwd';
GRANT ALL PRIVILEGES ON `ecomm_test_db`.* TO 'ecomm_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'ecomm_test'@'localhost';
FLUSH PRIVILEGES;
