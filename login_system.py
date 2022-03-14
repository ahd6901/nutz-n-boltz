import datetime

import utils
from getpass import getpass
from db_utils import *


def login_system_input(user_input):
    logged_in = [False, None]

    if user_input == "login" or user_input == "l":
        logged_in = login()

    elif user_input == "register" or user_input == "r":
        account_created = register()
        if account_created:
            logged_in = login("Successfully registered")
    return logged_in


def login(error_message=''):
    utils.clear_console()

    # Display
    print(error_message)
    print("Login")
    print()

    # User input
    username = input('Enter your username: ').strip()
    password = input('Enter your password: ').strip()  #Change to input() atm since getpass() prompt 'Enter your...' wasn't able to display on my end...
    valid_login = False
    # Check if valid login
    result = exec_get_one(
        "SELECT COUNT(username) FROM users WHERE username='{0}' AND password='{1}'".format(username, password))
    if result[0] == 1:
        valid_login = True
        exec_commit("UPDATE users SET last_accessed=CURRENT_TIMESTAMP WHERE username='{0}'".format(username))
        full_name = exec_get_one("SELECT first_name, last_name FROM users WHERE username='{0}'".format(username))
        user_id = exec_get_one("SELECT user_id FROM users WHERE username={0}'".format(username))
        print("Login successful!. Welcome back {0} {1} !".format(full_name[0], full_name[1]))

    if not valid_login:
        return login('Invalid login credentials. Please Retry')
    return [valid_login, username, user_id]


def register(error_message=''):
    utils.clear_console()

    # Display
    print(error_message)
    print("Register")
    print()

    # Get username (unique)
    while True:
        username = input('Enter your username: ').strip()
        if username == '' or username is None:
            print('Invalid username input. Please retry')
            continue
        username_found = exec_get_one("SELECT COUNT(username) FROM users WHERE username='{0}';".format(username))[0]
        if username_found != 0:
            print("username '{0}' is already taken. Please Retry".format(username))
            continue
        break

    first_name = input('Enter your first name: ').strip()
    # Check if first name is valid
    if first_name == '' or first_name is None:
        first_name = utils.reenter_invalid_input(
            'First name', first_name, 'Enter your first name: ')

    last_name = input('Enter your last name: ').strip()
    # Check if last_name is valid
    if last_name == '' or last_name is None:
        last_name = utils.reenter_invalid_input(
            'Last name', last_name, 'Enter your last name: ')

    # get email (unique)
    while True:
        email = input('Enter your email: ').strip()
        if username == '' or username is None or not utils.validate_email_format(email):
            print('Invalid email input. Please retry')
            continue
        username_found = exec_get_one("SELECT COUNT(email) FROM users WHERE email='{0}';".format(email))[0]
        if username_found != 0:
            print("email '{0}' is already taken.".format(email))
            continue
        break

    password = input('Enter your password: ').strip()
    password_confirmation = input('Confirm your password: ').strip()
    # check passwords entered match
    if password != password_confirmation:
        password = reenter_password()

    inputs_confirmed = confirm_input([username, first_name, last_name, email])

    now = datetime.datetime.now()
    exec_commit("INSERT INTO users(username, password, email, first_name, last_name, date_created,last_accessed) "
                "VALUES ('{0}','{1}','{2}','{3}','{4}','{5}','{6}');".format(username, password, email, first_name,
                                                                             last_name,
                                                                             now.strftime('%Y-%m-%d %H:%M:%S'),
                                                                             now.strftime('%Y-%m-%d %H:%M:%S')))
    if inputs_confirmed:
        user_created = True

    return user_created


def confirm_input(user_inputs):
    utils.clear_console()

    print(f'Username: {user_inputs[0]}')
    print(f'First Name: {user_inputs[1]}')
    print(f'Last Name: {user_inputs[2]}')
    print(f'Email: {user_inputs[3]}')

    confirmation_input = input('Confirm input (y/n/yes/no): ').strip()
    if confirmation_input not in ['y', 'yes', 'n', 'no']:
        return confirm_input(user_inputs)
    elif confirmation_input in ['y', 'yes']:
        return user_inputs
    else:
        return register()


def reenter_password():
    utils.clear_console()

    # Display
    print("Passwords did not match")
    print("Please reenter password")

    # User input
    password = input('Enter your password: ').strip()
    password_confirmation = input('Confirm your password: ').strip()

    if password != password_confirmation:
        return reenter_password()
    return password
