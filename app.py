import utils
import login_system_utils as login_utils

def run():
  logged_in = start_menu()
  if logged_in[0]:
    user_menu(logged_in[1])

def start_menu():
  utils.clear_console()

  # User input
  user_input = start_menu_input()
  logged_in = login_utils.login_system_input(user_input)
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

def user_menu(username):
  utils.clear_console()

  print(f'Welcome back {username}')


if __name__ == '__main__':
  run()
