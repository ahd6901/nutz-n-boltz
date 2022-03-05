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

def create_category(args):
  print('Action: Create Category')
  print(args)

def remove_category(args):
  print('Action: Remove Category')
  print(args)

def display_categories(args):
  print('Action: Display Categories')
  print(args)
