-- prepares a  test SQL server for grocerease


CREATE DATABASE IF NOT EXISTS grocerease;
CREATE USER IF NOT EXISTS 'grocer_dev'@'localhost' IDENTIFIED BY 'grocer_dev_pwd';
GRANT ALL PRIVILEGES ON `grocerease`.* TO 'grocer_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'grocer_dev'@'localhost';
FLUSH PRIVILEGES;
