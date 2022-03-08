import utils
from getpass import getpass
from db_utils import *
from datetime import date


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
    password = input('Enter your password: ').strip()
    valid_login = False
    # Check if valid login
    result = exec_get_one(
                "SELECT COUNT(username) FROM users WHERE username='{0}' AND password='{1}'".format(username, password))
    if result[0] == 1:
        valid_login = True
        exec_commit("UPDATE users SET last_accessed=CURRENT_TIMESTAMP WHERE username='{0}'".format(username))
        full_name = exec_get_one("SELECT first_name, last_name FROM users WHERE username='{0}'".format(username))
        print("Login successful!. Welcome back {0} {1} !".format(full_name[0], full_name[1]))

    if not valid_login:
        return login('Invalid login')
    return [valid_login, username]



def register(error_message=''):
    utils.clear_console()

    # Display
    print(error_message)
    print("Register")
    print()

    # User input
    username = input('Enter your username: ').strip()
    # Check if username is available
    # TODO Replace Trues with call to API to check if username is available
    username_available = True
    while (not username_available):
        username = utils.reenter_invalid_input(
            'Username', username, 'Enter your username: ', 'Username is not available')
        username_available = True
    if username == '' or username is None:
        username = utils.reenter_invalid_input(
            'Username', username, 'Enter your username: ')

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

    email = input('Enter your email: ').strip()
    # Check if email is valid
    while (not utils.validate_email_format(email)):
        email = utils.reenter_invalid_input(
            'Email', email, 'Enter your email: ')

    password = getpass('Enter your password: ').strip()
    password_confirmation = getpass('Confirm your password: ').strip()
    # check passwords entered match
    if password != password_confirmation:
        password = reenter_password()

    inputs_confirmed = confirm_input([username, first_name, last_name, email])

    # TODO Replace False with call to API create user
    user_created = False

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
    password = getpass('Enter your password: ').strip()
    password_confirmation = getpass('Confirm your password: ').strip()

    if password != password_confirmation:
        return reenter_password()
    return password
