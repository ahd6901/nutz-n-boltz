
import os
from logging import root

import utils
from db_utils import *
import login_system as login_sys
import menu_system as menu_sys
from access import *


def run():
    #exec_schema_file('src\schema.sql')
    logged_in = start_menu()
    if logged_in[0]:
        user_menu_system(logged_in[1])


def start_menu():
    utils.clear_console()
    user_input = start_menu_input()
    logged_in = login_sys.login_system_input(user_input)
    return logged_in


def start_menu_input(error_message=""):
    utils.clear_console()
    print('Welcome to Nutz and Boltz')
    print('Please login or create an account')
    print()
    # Diplay
    print(error_message)
    print('Valid inputs')
    print('Login: login or l')
    print('Register: register or r')
    print()

    # User input
    user_input = input(":: ").strip().lower()

    # Check if valid input
    valid_inputs = ['login', 'l', 'register', 'r']

    if (user_input in valid_inputs):
        return user_input
    else:
        return start_menu_input(f'Invalid Input: "{user_input}"')


def user_menu_system(username):
    utils.clear_console()

    print(f'Welcome back {username}')

    menus = menu_sys.create_menus()
    current_menu = menus.get('User Menu')

    logout = False

    # Actions:
    # goto <menu_name>
    # logout
    # display actions
    # display menus

    goto_actions_map = {
        'goto user menu': menus.get('User Menu'),
        'goto requests menu': menus.get('Requests Menu'),
        'goto category menu': menus.get('Category Menu'),
        'goto catalog menu': menus.get('Catalog Menu'),
    }

    current_menu.display_menu()
    while logout != True:
        menu_actions_map = {
            'display menus': menu_sys.display_menus,
            'display actions': current_menu.display_actions
        }
        user_input = str(input(':: ')).strip().lower().split()

        if (len(user_input) == 1 and user_input[0] == 'logout'):
            logout = True
            break

        utils.clear_console()
        if (len(user_input) > 0):
            if (user_input[0] in current_menu.get_actions()):
                current_menu.display_menu()
                current_menu.get_action(user_input[0])(user_input)
            elif (len(user_input) == 2 and f'{user_input[0]} {user_input[1]}' in menu_actions_map.keys()):
                current_menu.display_menu()
                menu_actions_map.get(f'{user_input[0]} {user_input[1]}')()
            elif (
                    len(user_input) == 3 and f'{user_input[0]} {user_input[1]} {user_input[2]}' in goto_actions_map.keys()):
                current_menu = goto_actions_map.get(f'{user_input[0]} {user_input[1]} {user_input[2]}')
                current_menu.display_menu()
            else:
                current_menu.display_menu()
                print("Invalid User Input")
        else:
            current_menu.display_menu()
            print("Invalid User Input")
    exit_program()


def exit_program():
    print('Program Closing')


if __name__ == '__main__':
    run()
