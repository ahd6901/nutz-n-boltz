import utils
import login_system as login_sys
import menu_system as menu_sys
import psycopg2
from sshtunnel import SSHTunnelForwarder


# Establish connection to db
def connection(server):
    server.start()
    params = {
        'database': 'p320_13',
        'user': authenticator[0],
        'password': authenticator[1],
        'host': 'localhost',
        'port': server.local_bind_port,
        'options': f'-c search_path=p320_13',
    }
    conn = psycopg2.connect(**params)
    print("Database connection established")
    return conn


#Entrance to the program
def run():
    with open('credentials.txt') as f:
        global authenticator
        authenticator = [line.strip() for line in f]
        with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                                ssh_username=authenticator[0],
                                ssh_password=authenticator[1],
                                remote_bind_address=('localhost', 5432)) as server:
            print("SSH tunnel established")
            try:
                connect = connection(server)
                print("Welcome! Please select one of the following options:")
                while True:
                    print("1: Login to account")
                    print("2: Create new account")
                    print("3: Exit the Program")
                    option = input('>')
                    if option.strip() == '1':
                        pass
                        #logged_in_username=login(connect)
                        #insert entrance to the command menu here
                    elif option.strip() == '2':
                        pass
                        #register(connect)
                    elif option.strip() == '3':
                        pass
                        #quit(connect)
                    else:
                        print('invalid command. Please Try again')
            except Exception as e:
                print(str(e))
                #quit_program(connect)
            finally:
                pass
                #quit_program(connect)

    # logged_in = start_menu()
    # if logged_in[0]:
    #     user_menu_system(logged_in[1])


def start_menu():
    utils.clear_console()

    # User input
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
        return start_menu_input(f'Invalid input: "{user_input}"')


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
        user_input = input(":: ").strip().lower()
        if (user_input == 'logout'):
            logout = True
            break
        utils.clear_console()

        if (user_input in goto_actions_map.keys()):
            current_menu = goto_actions_map.get(user_input)
            current_menu.display_menu()
        elif (user_input in menu_actions_map.keys()):
            current_menu.display_menu()
            menu_actions_map.get(user_input)()
        elif (user_input in current_menu.get_actions()):
            current_menu.display_menu()
            current_menu.get_action(user_input)()
        else:
            current_menu.display_menu()
            print("Invalid user input")


if __name__ == '__main__':
    run()
