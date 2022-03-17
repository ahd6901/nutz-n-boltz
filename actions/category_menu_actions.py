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
    'create_category': 'create_category <category_name>',
    'remove_category': 'remove_category <category_name>',
    'display_categories': 'display_categories',
    'add_category_to_tool': 'add_category_to_tool <tool_id> <category_name>',
    'remove_category_from_tool': 'remove_category_from_tool <tool_id> <category_name>'
  }
  return input_map

def create_category(args, userid):
  # REQ:3
  print('Action: Create Category')
  action = args[0]
  if (len(args) == 2 and args[1]):
    name = args[1]
    checking_category = exec_get_one(f'SELECT name FROM categories WHERE owner_id = {userid} AND name = {name}')
    if (len(checking_category) > 0):
      print('Category Already Exists')
    else:
      print(args, userid) # TODO Test Print Remove 
      rows = exec_commit(f'INSERT INTO categories(owner_id, name) VALUES ({userid}, {name})')
      print('Insert',rows) # TODO Test Print Remove 
  elif (len(args) < 2):
    too_few_args(action)
  elif (len(args) > 2):
    too_many_args(action)


def remove_category(args, userid):
  # REQ:3
  print('Action: Remove Category')
  action = args[0]
  if (len(args) == 2 and args[1]):
    name = args[1]
    print(args, userid) # TODO Test Print Remove 
    checking_category = exec_get_one(f'SELECT name FROM categories WHERE owner_id = {userid} AND name = {name}')
    if (len(checking_category) == 0):
      print('Category Does Not Exist')
    else:
      rows = exec_commit(f'DELETE FROM categories WHERE owner_id = {userid} AND name = {name}')
      print('Delete',rows) # TODO Test Print Remove 
  elif (len(args) < 2):
    too_few_args(action)
  elif (len(args) > 2):
    too_many_args(action)

def display_categories(args, userid):
  # REQ:3
  print('Action: Display Categories')
  action = args[0]
  if (len(args) == 1):
    print(args, userid) # TODO Test Print Remove 
    rows = exec_get_all(f'SELECT name FROM categories WHERE owner_id = {userid} ORDER BY name ASC;')
    print('Categories----')
    [print(row[0]) for row in rows]
    print('---------------')
  else:
    too_many_args(action)


def add_category_to_tool(args, userid):
  # REQ:3
  print('Action: Add Category To Tool')
  print(args, userid) # TODO Test Print Remove 
  action = args[0]
  if (len(args) < 2):
    too_few_args(action)
    return

  if (len(args) > 2):
    too_many_args(action)
    return

  if (len(args) == 2 and args[1].isdigit() and args[2]):
    tool_id = args[1]
    category_name = args[2]
    checking_tool = exec_get_one(f'SELECT tool_id FROM tools WHERE tool_id = {tool_id}')
    print('Checking Tool', checking_tool)
    if (len(checking_tool) == 0): 
      print(f'Tool Not Found with ID: {tool_id}')
      return
    
    category_id = exec_get_one(f'SELECT id FROM categories WHERE owner_id = {userid} AND name = {category_name}')[0]
    print('Category Id', category_id)
    if (len(category_id) == 0):
      print(f'Category {category_name} Not Found')
      return

    checking_category = exec_get_one(f'SELECT category_id FROM categorized_tools WHERE category_id = {category_id} AND tool_id = {tool_id}')
    print('Checking Category', checking_category)
    if (len(checking_category) > 0):
      print(f'Tool ({tool_id}) Already Exists In Category {category_name}')
      return
    
    rows = exec_commit(f'DELETE FROM categorized_tools WHERE category_id {category_id} AND tool_id = {tool_id})')
    print('Delete',rows) # TODO Test Print Remove 


def remove_category_from_tool(args, userid):
  # REQ:3
  print('Action: Remove Category From Tool')

  action = args[0]

  if (len(args) < 2):
    too_few_args(action)
    return

  if (len(args) > 2):
    too_many_args(action)
    return
  
  if (len(args) == 2 and args[1].isdigit() and args[2]):
    tool_id = args[1]
    category_name = args[2]
    checking_tool = exec_get_one(f'SELECT tool_id FROM tools WHERE tool_id = {tool_id}')
    print('Checking Tool', checking_tool)
    if (len(checking_tool) == 0): 
      print(f'Tool Not Found with ID: {tool_id}')
      return
    
    category_id = exec_get_one(f'SELECT id FROM categories WHERE owner_id = {userid} AND name = {category_name}')[0]
    print('Category Id', category_id)
    if (len(category_id) == 0):
      print(f'Category {category_name} Not Found')
      return
    
    checking_category = exec_get_one(f'SELECT category_id FROM categorized_tools WHERE category_id = {category_id} AND tool_id = {tool_id}')
    print('Checking Category', checking_category)
    if (len(checking_category) == 0):
      print(f'Category {category_name} Not Found On Tool with ID: {tool_id}')
      return
    
    category_id = checking_category[0]
    rows = exec_commit(f'INSERT INTO categorized_tools(category_id, tool_id) VALUES ({category_id}, {tool_id})')
    print('Insert',rows)

def too_many_args(action):
  print(f'Too many Arguments')
  print(action_input_map().get(action))

def too_few_args(action):
  print('Too Few Arguments')
  print(action_input_map().get(action))
