from json import tool
from sre_constants import CATEGORY_WORD
from unicodedata import category
from db_utils import exec_get_one, exec_get_all, exec_commit
from re import search, findall
from datetime import date
import random


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

  today = date.today()
  d = today.strftime("%Y-%m-%d")

  name = input("Tool Name: ")
  desc = input("Description of tool: ")
  price = round(float(input("Tool Price: ")),2)
  shareinput = input("Sharable? (t/f): ")
  availinput = input("Available to share? (t/f): ")


  if shareinput == "t":
    sharable = True
  elif shareinput == "f":
    sharable = False
  else:
    print("Must choose t or f")
    return

  if availinput == "t":
    available = True
  elif availinput == "f":
    available = False
  else:
    print("Must choose t or f")
    return

  try:

    exec_commit("INSERT INTO tools(times_lent,barcode,name,description,shareable,purchase_price,purchase_date,available) VALUES\
      ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}');".format(0,random.randint(0,999999999),name,desc,sharable,price,d,available))

    max_toolid = int(exec_get_one("SELECT MAX(tool_id) from tools")[0])
    
    exec_commit("INSERT INTO catalog_tools(owner_id, tool_id) VALUES ('{0}', '{1}');".format(userid,max_toolid))
    print("Tool Added to catalog!")
  except Exception as e:
    print('Error Adding Tool to Catalog', e)
    return

  return

def sort_tools(args, userid):
  # REQ:5
  print('Action: Sort Tools')
  print("usage: sort_tools")
  print(args)

  tuples = []

  colinput = input("Name or Category? (name/category/tool_id): ")
  sortinput = input("Ascending or Descending? (ASC/DESC): ")

  tuples = exec_get_all("SELECT tool_id, name, description FROM tools ORDER BY {0} {1};".format(colinput,sortinput))
  cols = ["tool_id","name","description"]
  print_tuples(cols,tuples)


def remove_tool(args, userid):
  # REQ:2 / 12
  print('Action: Remove Tool')
  print(args)

  toolid = input("ID of tool to remove: ")

  tool_exists = exec_get_one("SELECT COUNT(tool_id) FROM tools WHERE tool_id='{0}'".format(toolid))

  if tool_exists:
    try:
      exec_commit("DELETE FROM catalog_tools WHERE tool_id = '{0}';".format(toolid))
      print("Tool Removed from Catalog!")
    except Exception as e:
      print('Error Removing Tool From Catalog', e)
      return
  else:
    print("Tool does not exist")

  return

def update_tool(args, userid):
  # REQ:2
  print('Action: Update Tool')
  print('usage: update_tool <tool_id>')

  if len(args) != 2:
    print("Incorrect amount of arguments")
    return

  tool_exists = exec_get_one("SELECT COUNT(tool_id) FROM tools WHERE tool_id='{0}'".format(args[1]))

  if tool_exists:
    try:

      tool = exec_get_one("SELECT tool_id,times_lent,barcode,name,description,shareable,purchase_price,purchase_date,available from tools where tool_id='{0}';".format(args[1]))
      print_tuple(["tool_id","times_lent","barcode","name","description","shareable","purchase_price","purchase_date","available"], tool)

      cols = ["times_lent","barcode","name","description","shareable","purchase_price","purchase_date","available"]

      print("times_lent, barcode, name, description, sharable, purchase_price, purchase_date, available")
      col = input("Column to update: ")

      if col in cols:
        val = input("Value: ")
        exec_commit("UPDATE tools SET {0} = '{1}' where tool_id = {2}".format(col,val,int(args[1])))
        print("Updated tool")

        tool = exec_get_one("SELECT tool_id,times_lent,barcode,name,description,shareable,purchase_price,purchase_date,available from tools where tool_id='{0}';".format(args[1]))
        print_tuple(["tool_id","times_lent","barcode","name","description","shareable","purchase_price","purchase_date","available"], tool)

        return
      else:
        print("Choose from available columns to set")
    except Exception as e:
      print('Error Updating tool', e)
      return
  else:
    print("Tool does not exist")
    return


def search_tool(args, userid):
  # REQ:4
  print('Action: Search Tool')

  search_terms = []

  if len(args) > 1:
    if args[1].lower() == "name" or args[1].lower() == "category":
      for j in range(2,len(args)):
        search_terms.append(args[j].capitalize())
        search_terms.append(args[j].lower())
        print("added search term {0}".format(args[j]))
    elif args[1] == "barcode":
      search_terms.append(args[2])
    else:
      print("usage: search_tool <name/barcode/category> <query> (showall)")
      return
  else:
    print("usage: search_tool <name/barcode/category> <query> (showall)")
    return

  tuples = []

  if args[1].lower() == "name":
    cols = ["tool_id", "name", "description"]
    tuples = exec_get_all("SELECT tool_id, name, description from tools where name like '%%_{0}%%'".format(search_terms[0][1:]))
    print_tuples(cols,tuples)

  elif args[1].lower() == "category":
    category_tup = exec_get_all("SELECT category_id, name from categories where name like '%%_{0}%%'".format(args[2]))
    print("Getting tools in category {0}".format(category_tup[0][1]))
    tools_in_category = exec_get_all("SELECT tool_id from categorized_tools where category_id = '{0}'".format(category_tup[0][0]))
    for tool in tools_in_category:
      tuples.append(exec_get_one("SELECT tool_id, name, description from tools where tool_id = '{0}'".format(int(tool[0]))))
  
    tuples = list(set(tuples) | set(tuples))
    cols = ["tool_id","name","description"]
    print_tuples(cols,tuples)

  else:
    cols = ["tool_id", "name", "description"]
    tuples = exec_get_all("SELECT tool_id, name, description from tools where barcode = '{0}'".format(search_terms[0]))
    print_tuples(cols,tuples)

def return_tool(args, userid):
  # REQ: 11
  print('Action: Return Tool')
  print(args)

  today = date.today()
  d = today.strftime("%Y-%m-%d")

  toolid = input("ID of Tool to return: ")

  tool_exists = exec_get_one("SELECT COUNT(tool_id) FROM tools WHERE tool_id='{0}';".format(toolid))

  if tool_exists:
    try:
      exec_commit("UPDATE user_tool_requests SET date_returned = '{0}', date_status_changed = '{1}' WHERE tool_id = '{2}' and requesting_user_id = '{3}';".format(d,d,toolid,userid))
      print("Tool Returned!")
    except Exception as e:
      print('Error Returning Tool', e)
      return
  else:
    print("Tool does not exist")

  return

def print_tuples(cols,tuples):
  for col in cols:
    print(col+"\t\t\t",end="")
  print('\n')
  for tup in tuples:
    for val in tup:
      if len(str(val)) < 4:
        print(str(val)+"\t\t", end="")
      elif len(str(val)) < 23:
        print(str(val)+"\t\t\t", end="")
      else:
        print(str(val)[:27]+"...\t\t",end="")
    print("\n")


def print_tuple(cols,tuple):
  for col in cols:
    print(col+"\t\t\t",end="")
  print('\n')
  for val in tuple:
    if len(str(val)) < 4:
      print(str(val)+"\t\t", end="")
    elif len(str(val)) < 23:
      print(str(val)+"\t\t\t", end="")
    else:
      print(str(val)[:27]+"...\t\t",end="")
  print("\n")

