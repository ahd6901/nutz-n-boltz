from traceback import print_tb
from db_utils import exec_get_one, exec_get_all, exec_commit

def action_input_map():
  input_map = {
    'logout': 'logout',
    'display menus': 'display menus',
    'display actions': 'display actions',
    'goto user menu': 'goto user menu',
    'goto requests menu': 'goto requests menu',
    'goto category menu': 'goto category menu',
    'goto catalog menu': 'goto catalog menu',
    'create_category': 'create_category',
    'remove_category': 'remove_category <category_name>',
    'display_categories': 'display_categories',
    'add_category_to_tool': 'add_category_to_tool'
  }
  return input_map

def create_category(args, userid):
  # REQ:3
  print('Action: Create Category')
  print(args)
  tuples = exec_get_all('SELECT * FROM users')
  print(tuples)

def remove_category(args, userid):
  # REQ:3
  print('Action: Remove Category')
  print(args)

def display_categories(args, userid):
  # REQ:3
  print('Action: Display Categories')
  
  print(args)

def add_category_to_tool(args, userid):
  # REQ:3
  print('Action: Add Category To Tool')
  print(args)
