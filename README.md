README -
This is the final project for CS 121 Relational Databases at Caltech.
The goal of the project was to create a database that facilitated searching
for soccer players based on specific criteria. The database supports a
certain number of command-line queries as well as manager logins. Follow
the instructions below to try it out for yourself. Thank you!

Contributors: Mario Solis and Julian Navarro Rodriguez

Data source:
https://www.kaggle.com/datasets/davidcariboo/player-scores

NOTE: THIS PROGRAM IS TESTED ON MYSQL 8.0.

Instructions for loading data on command-line:
Make sure you have MySQL downloaded and available through your
device's command-line.

First, enter MySQL:

    sudo mysql --local-infile=1

Not including the "mysql>" prompt, run the following lines of code on your command-line
to create an appropriate database in mySQL.

    mysql> CREATE DATABASE manageriodb;
    mysql> USE manageriodb;
    mysql> SOURCE setup-managerio.sql;
    mysql> quit;

If there are errors involving the load-data.sql file, run all of the previous lines one more time.

Instructions for Python program:
Please install the Python MySQL Connector using the following line if not installed already.

    $ pip install mysql-connector-python

After loading the data and verifying you are in the correct database, 
run the following to open the Python application:

    $ python3 app.py

For the admin side, please log in with the following credentials:

    username = managerio_admin
    password = messi#1

For the client side, please log in with the following user/passwords
or create your own account.

The following managers are registered by default:

    USERNAME | PASSWORD     | CLUB
    msolis   | Pizza25      | Futbol Club Barcelona
    jnavarro | Husky001     | Paris Saint-Germain Football Club
    boliveir | EuropaChamps | Sevilla Fútbol Club S.A.D.
    cgarrido | aguerooo     | Manchester City Football Club
    rcrespo  | ynwa2024     | Liverpool Football Club

Here is a suggested guide to using the client side:
1. Select option [s] to find stats for an outfield player.
2. Select option [g] to find stats for an goalkeeper.
3. Select option [b] to find players within your budget.
4. Select option [n] to find players based on nationality.
4. Select option [a] to find players based on age.
5. Select option [p] to outfield players based on position.
6. Select option [q] to quit.

Here is a suggested guide to using the admin side:
1. Select option [p] to change a manager's password.
2. Select option [m] to see currently signed up managers.
3. Select option [a] to add a new player to the database.
3. Select option [l] to go back to the login screen.
3. Select option [q] to quit.

Files written to user's system:
- No files are written to the user's system.

Unfinished features:

- Making queries involving searching for multiple players at the same time.
