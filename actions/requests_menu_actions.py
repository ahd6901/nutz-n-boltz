from urllib import request
from db_utils import exec_get_one, exec_get_all, exec_commit
from datetime import date

def action_input_map():
  input_map = {
    'logout': 'logout',
    'display menus': 'display menus',
    'display actions': 'display actions',
    'goto user menu': 'goto user menu',
    'goto requests menu': 'goto requests menu',
    'goto category menu': 'goto category menu',
    'goto catalog menu': 'goto catalog menu',
    'respond_to_request': 'respond_to_request',
    'request_tool': 'request_tool',
    'manage_requests': 'manage_requests'
  }
  return input_map

def respond_to_request(args, userid):
  # REQ:8
  print('Action: Respond to Request')
  print(args)


  requesting_users = []
  incoming_req_tuples = get_incoming_requests(userid)
  if len(incoming_req_tuples) != 0:
    for tuple in incoming_req_tuples:
      requesting_users.append(tuple[0])
    
    print_requests(userid,True)
  else:
    print("No Requests to respond to")
    return

  print(requesting_users)

  today = date.today()
  d = today.strftime("%Y-%m-%d")

  reqid = int(input("ID of user to respond to: "))
  status = input("Response to request (accepted/declined): ")

  if reqid in requesting_users:
    try:
      exec_commit("UPDATE user_tool_requests SET status = '{0}', date_status_changed = '{1}', date_borrowed = '{2}' WHERE requesting_user_id = '{3}'".format(status,d,d,reqid))
      print("Updated Status")
    except Exception as e:
      print("Error updating request", e)
      return
  if len(requesting_users) > 1:
    print_requests(userid,True)
  

def request_tool(args, userid):
  # REQ:6
  print('Action: Request Tool')
  print(args)

  today = date.today()
  d = today.strftime("%Y-%m-%d")

  toolid = input("ID of Tool to borrow")
  reqdate = input("Date required (yyyy-mm-dd): ")
  returndate = input("Date to return (yyyy-mm-dd): ")

  try:
    exec_commit("INSERT INTO user_tool_requests(requesting_user_id,tool_id,date_required,status,overdue,date_status_changed,duration,expected_return_date) VALUES ({0},{1},'{2}','pending',false,'{3}',1,'{4}');".format(userid,toolid,reqdate,d,returndate))
    print("Request Added")
  except Exception as e:
    print("Error adding request", e)
    return

def manage_requests(args, userid):
  # REQ:7
  print('Action: Request Tool')
  print(args)

  print("Incoming requests:")
  print_requests(userid,True)
  print("Outgoing requests:")
  print_requests(userid,False)

def get_incoming_requests(userid):
  request_tuple = exec_get_all("SELECT r.requesting_user_id, t.name, r.date_required, r.status, r.expected_return_date,r.date_status_changed from user_tool_requests r inner join tools t on t.tool_id = r.tool_id inner join catalog_tools c on t.tool_id = c.tool_id where c.owner_id = '{0}' and r.status = 'pending'".format(userid))
  return request_tuple

def get_outgoing_requests(userid):
  request_tuple = exec_get_all("SELECT r.requesting_user_id, t.name, r.date_required, r.status, r.expected_return_date, r.date_status_changed from user_tool_requests r inner join tools t on t.tool_id = r.tool_id where r.requesting_user_id = '{0}'".format(userid))
  return request_tuple

def print_requests(userid,incoming):
  # get open requests for a user's tools

  if incoming:
    request_tuple = get_incoming_requests(userid)
  else:
    request_tuple = get_outgoing_requests(userid)

  print("Requester ID \tTool Name \t\tDate Required\t\t Status \t\t Expected Return Date \t\t Last Status Change")

  for tuple in request_tuple:
    for val in tuple:
      print(str(val)[:18], end="\t\t")

    print("\n")

