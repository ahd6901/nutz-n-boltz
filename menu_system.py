from inspect import getmembers, isfunction
from actions import requests_menu_actions, catalog_menu_actions, category_menu_actions, user_menu_actions

def create_menus():
  user_menu = Menu('User Menu', getmembers(user_menu_actions, isfunction), user_menu_actions.action_input_map())
  requests_menu = Menu('Requests Menu', getmembers(requests_menu_actions, isfunction), requests_menu_actions.action_input_map())
  category_menu = Menu('Category Menu', getmembers(category_menu_actions, isfunction), category_menu_actions.action_input_map())
  catalog_menu = Menu('Catalog Menu', getmembers(catalog_menu_actions, isfunction), catalog_menu_actions.action_input_map())
  
  menus = {
    'User Menu': user_menu,
    'Requests Menu': requests_menu,
    'Category Menu': category_menu,
    'Catalog Menu': catalog_menu
  }
  return menus

def create_action_map(function_list):
  action_map = {}
  for function in function_list:
    action_map[function[0]] = function[1]
  return action_map

def display_menus():
  print('Menus List:')
  for menu in ['User Menu', 'Requests Menu', 'Category Menu', 'Catalog Menu']:
    print(menu)
  print()

class Menu():
  def __init__(self, name, actions, action_inputs):
    self.name = name
    self.actions = create_action_map(actions)
    self.action_inputs = action_inputs

  def get_name(self):
    return self.name

  def get_actions(self):
    return self.actions.keys()

  def get_action(self, action_name):
    return self.actions.get(action_name)

  def display_actions(self):
    print(f'{self.name} Actions:')
    if (type(self.action_inputs) is not dict or len(self.action_inputs) == 0):
      print('No actions found')
    else:
      for action in self.action_inputs.values():
        print(f'{action}')
    print()
    
  def display_menu(self):
    print(f'Menu: {self.name}')
    print()

  def __str__(self):
    return self.get_name()
