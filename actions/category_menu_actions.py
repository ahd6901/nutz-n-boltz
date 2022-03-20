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
    category_name = args[1]
    checking_category_exists = exec_get_one(f"SELECT name FROM categories WHERE owner_id = {userid} AND name = '{category_name}'")
    if (checking_category_exists):
      print(f'Category {category_name} Already Exists')
    else: 
      try:
        exec_commit(f"INSERT INTO categories(owner_id, name) VALUES ({userid}, '{category_name}')")
      except Exception as e:
        print('Error Creating category', e)
        return
      print(f"Category {category_name} Created")
  elif (len(args) < 2):
    too_few_args(action)
  elif (len(args) > 2):
    too_many_args(action)


def remove_category(args, userid):
  # REQ:3
  print('Action: Remove Category')
  action = args[0]
  if (len(args) == 2 and args[1]):
    category_name = args[1]
    checking_category_exists = exec_get_one(f"SELECT name FROM categories WHERE owner_id = {userid} AND name = '{category_name}'")
    if (checking_category_exists):
      try: 
        exec_commit(f"DELETE FROM categories WHERE owner_id = {userid} AND name = '{category_name}'")
      except Exception as e:
        print('Error Removing category', e)
        return
      print(f'Category {category_name} deleted successfully')
    else:
      print(f'Category {category_name} Does Not Exist')
  elif (len(args) < 2):
    too_few_args(action)
  elif (len(args) > 2):
    too_many_args(action)


def display_categories(args, userid):
  # REQ:3
  print('Action: Display Categories\n')
  action = args[0]
  if (len(args) == 1):
    rows = exec_get_all(f"SELECT name FROM categories WHERE owner_id = {userid} ORDER BY name ASC;")
    print('Categories-----\n')
    if (len(rows) == 0):
      print('No categories found')
    [print(row[0]) for row in rows]
    print('\n---------------')
  else:
    too_many_args(action)


def add_category_to_tool(args, userid):
  # REQ:3
  print('Action: Add Category To Tool')
  action = args[0]
  if (len(args) < 3):
    too_few_args(action)
    return

  if (len(args) > 3):
    too_many_args(action)
    return

  if (len(args) == 3 and args[1].isdigit() and args[2]):
    tool_id = args[1]
    category_name = args[2]
    checking_tool = exec_get_one(f"SELECT tool_id FROM catalog_tools WHERE owner_id = {userid} AND tool_id = {tool_id}")
    if (not checking_tool): 
      print(f'Tool Not Found with ID: {tool_id} In Your Catalog')
      return
    
    category_id = exec_get_one(f"SELECT category_id FROM categories WHERE owner_id = {userid} AND name = '{category_name}'")
    if (not category_id):
      print(f'Category {category_name} Not Found')
      return
    category_id = category_id[0]
    checking_category_assigned = exec_get_one(f"SELECT category_id FROM categorized_tools WHERE category_id = {category_id} AND tool_id = {tool_id}")
    if (checking_category_assigned):
      print(f'Tool ({tool_id}) Already Exists In Category {category_name}')
      return
    try:
      exec_commit(f'INSERT INTO categorized_tools(category_id, tool_id) VALUES ({category_id}, {tool_id})')
    except Exception as e:
      print('Error Adding Tool to Category', e)
      return
    print(f'Category {category_name} Successfully Added To Tool With ID: {tool_id}')


def remove_category_from_tool(args, userid):
  # REQ:3
  print('Action: Remove Category From Tool')

  action = args[0]

  if (len(args) < 3):
    too_few_args(action)
    return

  if (len(args) > 3):
    too_many_args(action)
    return
  
  if (len(args) == 3 and args[1].isdigit() and args[2]):
    tool_id = args[1]
    category_name = args[2]
    checking_tool = exec_get_one(f"SELECT tool_id FROM catalog_tools WHERE owner_id = {userid} AND tool_id = {tool_id}")
    if (not checking_tool): 
      print(f'Tool Not Found with ID: {tool_id} In Your Catalog')
      return
    
    category_id = exec_get_one(f"SELECT category_id FROM categories WHERE owner_id = {userid} AND name = '{category_name}'")
    if (not category_id):
      print(f'Category {category_name} Not Found')
      return
    
    category_id = category_id[0]
    checking_category_assigned = exec_get_one(f"SELECT category_id FROM categorized_tools WHERE category_id = {category_id} AND tool_id = {tool_id}")
    if (not checking_category_assigned):
      print(f'Category {category_name} Not Found On Tool with ID: {tool_id}')
      return
    
    category_id = checking_category_assigned[0]
    try:
      exec_commit(f"DELETE FROM categorized_tools WHERE category_id = {category_id} AND tool_id = {tool_id}")
    except Exception as e:
      print('Error Removing Tool From Category', e)
      return
    print(f'Category {category_name} Successfully Removed From Tool With ID: {tool_id}')

def too_many_args(action):
  print(f'Too many Arguments')
  print(action_input_map().get(action))

def too_few_args(action):
  print('Too Few Arguments')
  print(action_input_map().get(action))
