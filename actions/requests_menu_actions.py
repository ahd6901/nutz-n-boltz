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
    'respond_to_request': 'respond_to_request <request_id> <response>',
    'request_tool': 'request_tool <tool_id> <user_id> <duration>',
    'manage_requests': 'manage_requests'
  }
  return input_map

def respond_to_request(args, userid):
  # REQ:8
  print('Action: Respond to Request')
  print(args)

def request_tool(args, userid):
  # REQ:6
  print('Action: Request Tool')
  print(args)

def manage_requests(args, userid):
  # REQ:7
  print('Action: Request Tool')
  print(args)