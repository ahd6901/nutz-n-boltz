def action_input_map():
  input_map = {
    'display menus': 'display menus',
    'display actions': 'display actions',
    'goto user menu': 'goto user menu',
    'goto requests menu': 'goto requests menu',
    'goto category menu': 'goto category menu',
    'goto catalog menu': 'goto catalog menu',
    'create_category': 'create_category',
    'remove_category': 'remove_category',
    'display_categories': 'display_categories'
  }
  return input_map

def create_category():
  print('Action: Create Category')

def remove_category():
  print('Action: Remove Category')

def display_categories():
  print('Action: Display Categories')
