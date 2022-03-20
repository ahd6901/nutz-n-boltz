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
    'add_tool': 'add_tool',
    'sort_tools': 'sort_tools <category/name> <asc/desc>',
    'remove_tool': 'remove_tool',
    'update_tool': 'update_tool',
    'search_tool': 'search_tool <barcode/name/category> <search-term>',
    'return_tool': 'return_tool'
  }
  return input_map

def add_tool(args, userid):
  # REQ:2
  print('Action: Add Tool')
  print(args, userid)

def sort_tools(args, userid):
  # REQ:5
  print('Action: Sort Tools')
  print(args)

def remove_tool(args, userid):
  # REQ:2 / 12
  print('Action: Remove Tool')
  print(args)

def update_tool(args, userid):
  # REQ:2
  print('Action: Update Tool')
  print(args)

def search_tool(args, userid):
  # REQ:4
  print('Action: Search Tool')
  print(args)

def return_tool(args, userid):
  # REQ: 11
  print('Action: Return Tool')
  print(args)
