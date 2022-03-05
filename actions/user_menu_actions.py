def action_input_map():
  input_map = {
    'display menus': 'display menus',
    'display actions': 'display actions',
    'goto user menu': 'goto user menu',
    'goto requests menu': 'goto requests menu',
    'goto category menu': 'goto category menu',
    'goto catalog menu': 'goto catalog menu',
    'show_stats': 'show_stats'
  }
  return input_map

def show_stats(args):
  print('Action: Show Stats')
  print(args)
