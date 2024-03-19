"""
Student name(s): Mario Solis and Julian Navarro
Student email(s): msolis@caltech.edu and jnavarro@caltech.edu
High-level program overview

******************************************************************************

Some sections are provided as recommended program breakdowns, but are optional
to keep, and you will probably want to extend them based on your application's
features.

specialization: player is goalkeeper XOR player is outfield player
every symbol matters
error handling makes UX nicer

TODO:
- For full credit, remove any irrelevant comments, which are included in the
  template to help you get started. Replace this program overview with a
  brief overview of your application as well (including your name/partners name).
  This includes replacing everything in this *** section!
******************************************************************************
"""
# TODO: Make sure you have these installed with pip3 if needed
import sys  # to print error messages to sys.stderr
import mysql.connector
# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. ***Set to False when done testing.***
DEBUG = True

# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='appadmin',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',  # this may change!
          password='admin_pass',
          database='manageriodb' # replace this with your database name
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database; hence the DEBUG use.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            # A fine catchall client-facing message.
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)

# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------

def find_stats():
    player_name = input('What is the name of the player you are looking for?\n')
    cursor = conn.cursor()
    sql = """
    S * FROM players NATURAL JOIN outfield_players WHERE player_name = '%s'; 
    """ % (player_name)
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred when searching for player stats.')
            return
    if not row:
        print('No results found.')
    else:
        print('Here are the stats of the player: \n')
        print("""Player ID: %d , Player Name: %s, Club ID: %d, Birthday: %s,
Nationality: %s, Market value: %d, Appearances: %d, Position: %s,
Goals: %d, Assists: %d, Passing accuracy: %d, Key passes per game: %d, Interceptions per game: %d
              """ % (row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                     row[7], row[8], row[9], row[10], row[11], row[12]))
        
def find_goalie_stats():
    player_name = input('What is the name of the goalkeeper you are looking for?\n')
    cursor = conn.cursor()
    sql = """
    SELECT * FROM players NATURAL JOIN goalkeepers WHERE player_name = '%s'; 
    """ % (player_name)
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred when searching for player stats.')
            return
    if not row:
        print('No results found.')
    else:
        print('Here are the stats of the player: \n')
        print("""Player ID: %d , Player Name: %s, Club ID: %d, Birthday: %s,
Nationality: %s, Market value: %d, Appearances: %d, Saves: %d, Clean sheets: %d
              """ % (row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                     row[7], row[8]))

def find_age():
    min_age = input('What is the minimum age you are looking for?\n')
    while not min_age.isnumeric():
        min_age = input("That's not a number! Enter again: ")
    max_age = input('What is the maximum age you are looking for?\n')
    while not max_age.isnumeric() or max_age < min_age:
        if not max_age.isnumeric():
            max_age = input("That's not a number! Enter again: ")
        else:
            max_age = input("Invalid maximum! Enter again: ")
    cursor = conn.cursor()
    sql = """
    SELECT *, get_age(birth_date) AS age
    FROM players
    GROUP BY player_id
    HAVING age BETWEEN %d AND %d
    ORDER BY age DESC, num_appearances DESC LIMIT 10; 
    """ % (min_age, max_age)
    try:
        cursor.execute(sql)
        row = cursor.fetchone()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred when searching for player stats.')
            return
    if not row:
        print('No results found.')
    else:
        print('Here are the stats of the player: \n')
        print("""Player ID: %d , Player Name: %s, Club ID: %d, Birthday: %s,
Nationality: %s, Market value: %d, Appearances: %d, Age: %d
              """ % (row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                     row[7]))

def find_budget():
    cursor = conn.cursor()
    username = input("What is your username? ")
    sql = "SELECT budget FROM managers WHERE username = '%s';" % (username)
    cursor.execute(sql)
    budget = cursor.fetchone()
    print(f"Your budget is {budget[0]}. Would you like to proceed or change your budget?")
    response = input ("  (p) Proceed\n  (c) Change budget \n")
    if response == 'p':
        sql = """
        SELECT * FROM players WHERE market_value <= %d LIMIT 5; 
        """ % (budget)
    else:
        new_budget = input("What is your new budget?\n")
        while not new_budget.isnumeric():
            new_budget = input("That's not a number! Enter again: ")
        update_sql = "UPDATE managers SET budget = %d WHERE username = '%s';" % (float(new_budget), username)
        sql = """
        SELECT * FROM players WHERE market_value <= %d LIMIT 5; 
        """ % (float(new_budget))
        cursor.execute(update_sql)
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred when searching for manager budget.')
            return
    if not rows:
        print('No results found.')
    else:
        print('Players found based on budget: \n')
        for row in rows:
            print("""Player ID: %d, Player Name: %s, Club ID: %d, Birthday: %s,
Nationality: %s, Market value: %d, Appearances: %d 
              """ % (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
            
def find_nat():
    nat_name = input('What nationality are you looking for in players?\n')
    cursor = conn.cursor()
    sql = """
    SELECT player_id, player_name, club_id, birth_date, market_value, num_appearances
    FROM players WHERE nationality = '%s' LIMIT 5; 
    """ % (nat_name)
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred when searching for player nationality.')
            return
    if not rows:
        print('No results found.')
    else:
        print('Here are the nationalities of the player: \n')
        for row in rows:
            print("""Player ID: %d, Player Name: %s, Club ID: %d, Birthday: %s,
Market value: %d, Appearances: %d \n
              """ % (row[0], row[1], row[2], row[3], row[4], row[5]))

def find_pos():   
    print("What position are you looking for in players?")
    pos_name = input('(D) Defender (M) Midfielder (F) Forward: ')
    cursor = conn.cursor()
    sql = """
    SELECT player_id, player_name, market_value
    FROM players NATURAL JOIN outfield_players WHERE position = '%s' LIMIT 5; 
    """ % (pos_name)
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred when searching for player positions.')
            return
    if not rows:
        print('No results found.')
    else:
        print("Here are the players' info: \n")
        for row in rows:
            print("""Player ID: %d, Player Name: %s, Market value: %d\n
              """ % (row[0], row[1],  row[2]))

# admins adding a player to the database
def add_player():
    print("What player do you want to add? \n")
    pos_name = input('Name of the player you want to add: \n')
    pos_player_club = input('What is club name? \n')
    pos_birth = input('What is the player birthday? (FORMAT: YYYY-MM-DD): \n')
    pos_nationality = input('What is the player nationality? (Give the whole country name, e.g. Mexico) \n')
    pos_market_val = input('What is the market value of the player? \n')
    while not pos_market_val.isnumeric():
            pos_market_val = input("That's not a number! Enter again: ")
    pos_num_appearances = input('What is the number of appearances of the player? \n')
    while not pos_num_appearances.isnumeric():
            pos_num_appearances = input("That's not a number! Enter again: ")

    cursor = conn.cursor()
    sql1 = """SELECT club_id FROM clubs WHERE club_name = '%s';""" % (pos_player_club)
    cursor.execute(sql1)
    club_id = cursor.fetchone()
    max_sql = "SELECT MAX(player_id) FROM players;"
    cursor.execute(max_sql)
    max_id = cursor.fetchone()
    sql = """
    INSERT INTO players
    VALUES (%i, '%s', %i, '%s', '%s', %d, %i); 
    """ % (int(max_id[0]) + 1, pos_name, int(club_id[0]), pos_birth, pos_nationality, float(pos_market_val), int(pos_num_appearances))
    try:
        cursor.execute(sql)
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred when searching for player positions.')
            return
    else:
        print("Player is added to system.\n")

# admins seeing currently signed up managers
def curr_managers():
    cursor = conn.cursor()
    sql = """
    SELECT manager_id, manager_name, IFNULL(budget, 0)
    FROM managers LIMIT 5; 
    """ 
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred when searching for managers.')
            return
    if not rows:
        print('No results found.')
    else:
        print("Here are the current managers: \n")
        for row in rows:
            print("""Manager ID: %i, Manager name: %s, budget: %d
              """ % (row[0], row[1], row[2]))

# admins updating player market values
def update_player_info():
    cursor = conn.cursor()
    play_name = input("What is the player's name?\n")
    market_value = input("What is the new market value?\n")
    while not market_value.isnumeric():
            market_value = input("That's not a number! Enter again: ")
    sql = """
    UPDATE players
    SET market_value = %i
    WHERE player_name = '%s';
    """ % (int(market_value), play_name)
    try:
        cursor.execute(sql)
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred when changing team information.')
            return
    else:
        print("All changes were successful.\n")

# admins changing password for managers
def change_pass():
    cursor = conn.cursor()
    username = input("Enter manager's username: ")
    new_password = input("Enter new password: ")
    sql = "CALL change_password('%s', '%s');" % (username, new_password)
    try:
        cursor.execute(sql)
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred when changing password information.')
            return
    else:
        print("Your password change was successful.\n")


# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
# Note: There's a distinction between database users (admin and client)
# and application users (e.g. members registered to a store). You can
# choose how to implement these depending on whether you have app.py or
# app-client.py vs. app-admin.py (in which case you don't need to
# support any prompt functionality to conditionally login to the sql database)

# login screen functionality
def login():
    """
    """
    cursor = conn.cursor()
    print('\nWelcome to Manager.io!\n')
    print('We are here to help managers find the players they need for their club.\n')
    print('How can we be of service today?')

    while True:
        print(' (1) user login')
        print(' (2) admin login')
        print(' (q) exit')

        input_choice = input().lower()
        # admin login
        if input_choice == '2':
            admin_username = 'managerio_admin'
            admin_password = 'messi#1'
            input_username = input(' Enter your admin username: ')
            input_password = input(' Enter your admin password: ')
            try:
                if input_username == admin_username and input_password == admin_password:
                    admin = True
                    break
                else:
                    print('That username and password was not correct. Please try again!\n')
            except mysql.connector.Error as err:
                if DEBUG:
                    sys.stderr(err)
                    sys.exit(1)
                else:
                    sys.stderr('Login error. Set DEBUG = True')
        # user login
        elif input_choice == '1':
            admin = False
            print('Do you want to create a new account or sign in?\n')
            account_response = input(' (1) Create an account\n (2) Sign in\n')
            # creating account
            if account_response == '1':
                new_user_name = input('What is your name?\n')
                new_username = input('What is your username?\n')
                new_password = input('What is your password?\n')
                new_club = input('What is your club name?\n')
                new_budget = input('What is your budget?\n')
                while not new_budget.isnumeric():
                    new_budget = input("That's not a number! Enter again: ")
                sql = '''CALL insert_manager('%s', '%s', '%s', '%s', %d);''' % (new_user_name, new_username, new_password, new_club, float(new_budget))
                cursor.execute(sql)
                break
            # signing in to existing
            elif account_response == '2':
                try_username = input(' Enter username: ')
                try_password = input(' Enter password: ')
                sql = '''SELECT authenticate('%s', '%s');''' % (try_username, try_password)
                try:
                    cursor.execute(sql)
                    correct_info = cursor.fetchone()
                    # login info is correct
                    if correct_info[0] == 1:
                        break
                    else:
                        print("Username or password is incorrect. Do you want to try again?\n")
                        response = input("Y/N: ")
                        if response == "Y":
                            login()
                        else:
                            quit_ui()
                except mysql.connector.Error as err:
                    if DEBUG:
                        sys.stderr(err)
                        sys.exit(1)
                    else:
                        sys.stderr('Login error. Set debug = True')
                break
        # quitting
        elif input_choice == 'q':
            quit_ui()
        else:
            print('Invalid! Try again.')

    if admin:
        print('\nWelcome, admin!')
        show_admin_options()
    else:
        print('\nWelcome, client!')
        show_options()

# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------

# options for managers in app
def show_options():
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort),
    sending a request to do <x>, etc.
    """
    while True:
        print('What would you like to do? ')
        print('  (s) - Find stats for an outfield player')
        print('  (g) - Find stats for a goalkeeper')
        print('  (b) - Find players in your budget')
        print('  (n) - Find players based on nationality')
        print('  (a) - Find players based on age')
        print('  (p) - Find outfield players based on position')
        print('  (l) - back to login')
        print('  (q) - quit')
        print()
        ans = input('Enter an option: ').lower()
        if ans == 'q':
            quit_ui()
        elif ans == 's':
            find_stats()
        elif ans == 'g':
            find_goalie_stats()
        elif ans == 'b':
            find_budget()
        elif ans == 'n':
            find_nat()
        elif ans == 'a':
            find_age()
        elif ans == 'p':
            find_pos()
        elif ans == 'l':
            login()
        else:
            print("That's not one of the options!")

# options for admins in app
def show_admin_options():
    """
    Displays options specific for admins, such as adding new data <x>,
    modifying <x> based on a given id, removing <x>, etc.
    """
    while True:
        print('What would you like to do? ')
        print('  (d) - See current managers')
        print('  (p) - Change manager password')
        print('  (m) - Update player market value')
        print('  (a) - Add new player')
        print('  (l) - back to login')
        print('  (q) - quit')
        print()
        ans = input('Enter an option: ').lower()
        if ans == 'l':
            login()
        elif ans == 'q':
            quit_ui()
        elif ans == 'd':
            curr_managers()
        elif ans == 'p':
            change_pass()
        elif ans == 'm':
            update_player_info()
        elif ans == 'a':
            add_player()

def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('Good bye!')
    exit()

def main():
    """
    Main function for starting things up.
    """
    login()

if __name__ == '__main__':
    # This conn is a global object that other functions can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    conn = get_conn()
    main()