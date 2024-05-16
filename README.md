# CS551Q_solo_assessment
This is the solo assessment for the course CSS551Q at the University of Aberdeen. The goal is to build a shopping website using the Django framework with Python.

The website is deployed the application on PythonAnyWhere with mysql, 
this is the site:  <https://weizhang12138.pythonanywhere.com>

## Installation
1) Clone the repository to your local machine.
2) Set up and activate the virtual environment. Navigate to the project folder and execute the following commands in the terminal:
``` bash
cd CS551Q_team_assessment/
pyenv local 3.10.7 # This sets the local version of Python to 3.10.7 (Optional)
python3 -m venv .venv # This creates the virtual environment
source .venv/bin/activate # This activates the virtual environment

```
3) Install the requirements by executing the following command in the terminal:
```
pip install -r requirements.txt
```
## DataBase: SQLite3

## Load the data
Create the tables though django framework
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

## Import Data
I have already import data into database. if you want to add more data , you can open the file 'shoppingwebsites/management/commands/import_data.py',modify it and import the data by execute the following commands in the terminal:
```
cd shoppingwebsites/management/commands
#if you want to delete all the data: 'python manage.py delete_products'
python manage.py import_data
```

## Running the Project
1)Navigate to the 'CS551Q_solo_assessment' folder and start the server.
```bash
python3 manage.py runserver 0.0.0.0:8000 # Use Ctrl+C to stop the server.
```

##author :Wei Zhang
##email: t02wz23@abdn.ac.uk

### Program Structure
The program is composed of two Django applications: shopping for site basic settings and shoppingwebsites for the website's detailed content.

**shopping Folder**: Contains basic site settings.

**static Folder**: Contains all the css files, which are referenced in other HTML files.

**features Folder**: Contains all BDD test files and test environment configuration files. If you want to run the BDD test please execute the following commands:
* Open the file **environment.py** on the folder features, change the **context.home_page_url** into your local host.
* Then execute the following commands in the terminal
```bash
behave #make sure you are now on CS551Q_solo_assessment/
```
* You will see the BDD test.

**shoppingwebsites Folder**: Details the website's content.

* The 'data' Folder: Stores initial data.(excel files and csv files)
* The 'models.py': Defines multiple database tables including Users, Products, Orders, Product_details, Order_details, shopping_cart and CustomUserManager.This data model provides the site with the basic functionality to perform user administration, browse products, place orders and manage shopping carts. Each model has associated fields to store the necessary data and is related by foreign keys to form a relational database structure. In addition, the models are defined with appropriate indexes to optimise query performance.
* The 'views': Handle all website routing requests, including but not limited to all website visits, searches, purchases, adding to carts, adding, deleting, changing, or subtracting various information, as well as operations with different permissions.

* The 'management'/'commands' Folder: Contains 'import_data.py' for importing initial data into the database according to the models' structure, with error handling and data formatting.

* 'migrations' Folder: Synchronizes the model classes with the database schema.

* The 'templates' folder includes the admin folder, registration folder and a series of web pages.These web pages display various product information, product recommendations, shopping carts, orders, and account information.The html file in the registration folder is responsible for user login, logout and registration functions. The files in the admin folder are responsible for viewing and editing all data such as: product information, order information, user information, and you can also view charts of various data.

* The 'tests' folder contains all the unitest files and test functionalities of the website.

**The 'manage.py'** file is utilized for starting the server and includes error handling features.

**The db.sqlite3** file is the database file containing the data from 'import_data.py' and the tables from 'models.py'.

**superuser**
email:admin@test.com
password:zhangwei123


**test user1**
email:551850757@qq.com
password:zw123456789


**test user2**
email:test2@test.com
password:test123456789


**staff**
email:staff@example.com
password:zw123456789
