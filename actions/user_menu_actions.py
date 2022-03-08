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
    'show_stats': 'show_stats',
    'inspect_available_tools': 'inspect_available_tools',
    'inspect_lent_tools':'inspect_lent_tools',
    'inspect_borrowed_tools' : 'inspect_borrowed_tools'
  }
  return input_map

def show_stats(args):
  print('Action: Show Stats')
  print(args)

def inspect_available_tools(args):
  #REQ: 10 a
  print('Action: inspect_available_tools')
  print(args)

def inspect_lent_tools(args):
  # REQ:10 b
  print('Action: inspect_lent_tools')
  print(args)

def inspect_borrowed_tools(args):
  # REQ:10 c
  print('Action: inspect_borrowed_tools')
  print(args)