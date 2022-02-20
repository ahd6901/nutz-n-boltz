def action_input_map():
  input_map = {
    'display menus': 'display menus',
    'display actions': 'display actions',
    'goto user menu': 'goto user menu',
    'goto requests menu': 'goto requests menu',
    'goto category menu': 'goto category menu',
    'goto catalog menu': 'goto catalog menu',
    'respond_to_request': 'respond_to_request <request_id> <response>',
    'request_tool': 'request_tool <tool_id> <user_id> <duration>'
  }
  return input_map

def respond_to_request(request, response):
  print('Action: Respond to Request')

def request_tool(tool, user, duration):
  print('Action: Request Tool')