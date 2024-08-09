-- prepares a  test SQL server for ecommerce

CREATE DATABASE IF NOT EXISTS ecommerce;
CREATE USER IF NOT EXISTS 'ecomm_dev'@'localhost' IDENTIFIED BY 'ecomm_dev_pwd';
GRANT ALL PRIVILEGES ON `ecommerce`.* TO 'ecomm_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'ecomm_dev'@'localhost';
FLUSH PRIVILEGES;
