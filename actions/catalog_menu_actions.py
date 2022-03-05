def action_input_map():
  input_map = {
    'display menus': 'display menus',
    'display actions': 'display actions',
    'goto user menu': 'goto user menu',
    'goto requests menu': 'goto requests menu',
    'goto category menu': 'goto category menu',
    'goto catalog menu': 'goto catalog menu',
    'add_tool': 'add_tool',
    'manage_categories': 'manage_categories',
    'sort_tools': 'sort_tools',
    'remove_tool': 'remove_tool',
    'update_tool': 'update_tool',
    'search_tool': 'search_tool',
    'return_tool': 'return_tool'
  }
  return input_map

def add_tool(args):
  print('Action: Add Tool')
  print(args)

def manage_categories(args):
  print('Action: Manage Categories')
  print(args)

def sort_tools(args):
  print('Action: Sort Tools')
  print(args)

def remove_tool(args):
  print('Action: Remove Tool')
  print(args)

def update_tool(args):
  print('Action: Update Tool')
  print(args)

def search_tool(args):
  print('Action: Search Tool')
  print(args)

def return_tool(args):
  print('Action: Return Tool')
  print(args)
