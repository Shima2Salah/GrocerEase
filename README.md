# GrocerEase - Your Convenient Grocery Shop

## Team Members

- **Ahmed Ibrahim Ali Ahmed**: Backend Developer
- **Habiba Fernas**: Backend Developer
- **Shimaa Salah Sayed Abdelrhman**: Database Administrator
- **Mohamed Arafa**: Frontend Developer

## Project Overview

**GrocerEase** is an online grocery shopping platform designed to provide a convenient, user-friendly experience for customers. The platform allows users to:

- Browse a wide range of grocery products categorized for easy navigation.
- Add products to a shopping cart, with real-time updates on cart contents and total cost.
- Apply discount codes or coupons during checkout.
- Choose from various payment methods, including credit/debit cards, and secure payment gateways.
- Track order status and delivery updates.

The admin panel provides tools for managing:

- **Products**: Add, edit, or delete products, update stock levels, and apply discounts.
- **Orders**: View and manage orders, update order status, and process returns or refunds.
- **Users**: Manage customer accounts, including viewing order history and handling customer queries.

## Learning Objectives

- **Ahmed**: Enhance understanding of RESTful API design and backend performance optimization using Flask.
- **Habiba**: Gain experience in secure user authentication, session management, and data encryption.
- **Shimaa**: Master advanced SQL techniques, including query optimization, database normalization, and data security.
- **Mohamed**: Develop a highly responsive, intuitive user interface, and ensure cross-browser compatibility.

## Technologies Used

### Backend

- **Flask**: A lightweight Python web framework used for building the backend APIs.
- **SQLAlchemy**: An ORM for managing database interactions within Flask.
- **Jinja2**: Flask's templating engine for dynamically rendering HTML pages.

### Database

- **MySQL**: A relational database used to store all data, including user information, products, orders, and categories.
- **Redis**: Used for caching and session management to improve performance.

### Frontend

- **HTML/CSS**: For structuring and styling the web pages.
- **Bootstrap**: A responsive framework to ensure the website looks good on all devices.
- **JavaScript**: For client-side interactivity and AJAX requests.

### Version Control

- **Git**: For tracking changes and managing source code.
- **GitHub**: For collaboration and project management, including issue tracking and code reviews.

### Third-Party Services

- **Stripe**: Considering integration for secure payment processing.
- **AWS S3**: Potentially used for storing user-uploaded images, such as product photos.

## Key Features

- **Product Catalog**: Categorized listings of available grocery products with details such as price, description, and images.
- **Shopping Cart**: A dynamic cart where users can add, remove, or update items before checkout.
- **Coupons & Discounts**: Functionality to apply coupons and view discounted prices in real-time.
- **Order Tracking**: Users can track the status of their orders from processing to delivery.
- **Admin Dashboard**: A secure admin interface for managing inventory, orders, and user accounts.

## Color Reference

| Color          | Hex Code                                                        |
| -------------- | --------------------------------------------------------------- |
| Example Yellow | ![#ffc107](https://via.placeholder.com/10/ffc107?text=+) #ffc107 |
| Example Green  | ![#198754](https://via.placeholder.com/10/198754?text=+) #198754 |

## Database Schema Overview

- **Users**: Stores user information including login credentials, address, and order history.
- **Products**: Contains details about each product, including category, price, stock level, and discount information.
- **Categories**: Used to organize products into logical groups for easier browsing.
- **Orders**: Captures order details such as user, products ordered, total price, and status.
- **Order Items**: A breakdown of products within each order.
- **Coupons**: Stores discount codes and associated rules.
- **Payments**: Tracks payment information, including method and status.

## Security Measures

- **User Authentication**: Implemented using Flask-Login, ensuring secure login and session management.
- **Data Encryption**: Sensitive user data, such as passwords, is encrypted using industry-standard practices.
- **Input Validation**: All user inputs are validated to prevent SQL injection and other common security vulnerabilities.

## Challenges Identified

- **Integration**: Ensuring smooth communication between the frontend and backend, particularly during asynchronous operations.
- **Database Management**: Handling complex queries and relationships efficiently without compromising performance.
- **Security**: Protecting user data through secure coding practices, encryption, and regular security audits.
- **Time Constraints**: The admin panel frontend and form validation features were not fully completed due to time limitations.

## Getting Started

### Prerequisites

- **Python 3.x**: Ensure that Python is installed on your system.
- **MySQL**: Set up a MySQL server for database management.
- **Git**: Install Git for version control.

### Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/yourusername/grocerease.git
    cd grocerease
    ```

2. **GrocerEase Setup Guide**:

    ```bash
    # Update and install Python 3.10
    sudo apt update
    sudo apt install python3.10
    python3.10 --version

    # Install net-tools
    sudo apt install -y net-tools

    # Set up Python virtual environment
    python3 -m venv venv
    source venv/bin/activate
    pip3 install flask

    # Install MySQLdb module version 2.0.x
    sudo apt-get install python3-dev libmysqlclient-dev zlib1g-dev pkg-config
    sudo pip3 install mysqlclient
    sudo apt-get install python3-mysql.connector

    # Deactivate virtual environment
    deactivate

    # Working with MySQL DB
    python3 -c "
    import MySQLdb
    print(MySQLdb.version_info)
    "

    # Install SQLAlchemy module version 1.4.x
    sudo pip3 install SQLAlchemy

    python3 -c "
    import sqlalchemy
    print(sqlalchemy.__version__)
    "

    # Install additional packages
    pip install Flask-SQLAlchemy python-dotenv PyMySQL
    pip install -U Flask-SQLAlchemy

    # Check MySQL service status and restart
    sudo service mysql status
    sudo service mysql restart

    # Insert tables and data into MySQL DB
    cat grocer_dump.sql | mysql -uroot -p

    sudo mysql -e "
    use grocerease;
    show tables;
    select * from grocerease.users;
    select * from grocerease.products;
    "

    cat setup_grocerease.sql | mysql -hlocalhost -uroot -p

    # Run the application
    sudo service mysql restart
    GROCER_MYSQL_USER=grocer_dev GROCER_MYSQL_PWD=grocer_dev_pwd GROCER_MYSQL_HOST=localhost GROCER_MYSQL_DB=grocerease GROCER_TYPE_STORAGE=db python3 -m web_dynamic.app

    # Run Python app
    python3 app.py

    # Run a simple HTTP server
    python3 -m http.server

    # If port 5000 is in use
    sudo lsof -i :5000
    sudo kill 9289 9776
    ```

### Usage

- **Admin Login**: Access the admin panel at `/admin` to manage products, orders, and users.
- **Shopping**: Users can browse products, add them to their cart, and proceed to checkout.

## Contributing

We welcome contributions to improve GrocerEase. Please follow the guidelines below:

1. **Fork the Repository**: Create a fork of the project to your GitHub account.
2. **Create a New Branch**: Work on your feature or bugfix in a new branch.
3. **Submit a Pull Request**: Once your changes are ready, submit a pull request for review.

## Authors

For any inquiries or support, please reach out to the project team members:

- **Ahmed Ibrahim Ali Ahmed**: eng.ahmedads@gmail.com
- **Habiba Fernas**: habibafernas@gmail.com
- **Shimaa Salah Sayed Abdelrhman**: shimaasalah91.13@gmail.com
- **Mohamed Hamdy Arafa**: mohamedhamdy994@gmail.com
