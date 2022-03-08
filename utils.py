import os
import re

def clear_console():
  pass
  #os.system('clear')


def validate_email_format(email):
  email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
  return email_regex.match(email)


def reenter_invalid_input(input_type, input_entered, input_message, invalid_message=''):
  # Display
  print()
  if invalid_message == '':
    print(f'{input_type} is invalid: "{input_entered}"')
  else:
    print(invalid_message)

  # User input
  new_input = input(input_message).strip()

  if new_input is None or new_input == '':
    return reenter_invalid_input(input_type, new_input, input_message, invalid_message)
  return new_input
