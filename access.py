from datetime import date
def login(connect):
    cursor = connect.cursor()
    while True:
        username = input("Enter username:")
        password = input("Enter password:")
        cursor.execute(
            "SELECT COUNT(username) FROM users WHERE username='{0}' AND password='{1}'".format(username, password))
        if cursor.fetchone()[0] == 1:
            break
        else:
            print("Username and Password entered is incorrect! Please try again!")
    cursor.execute("UPDATE users SET last_accessed=CURRENT_TIMESTAMP WHERE username='{0}'".format(username))
    connect.commit()
    cursor.execute("SELECT first_name, last_name FROM users WHERE username='{0}'".format(username))
    full_name = cursor.fetchone()
    print("Login successful!. Welcome back {0} {1} !".format(full_name[0], full_name[1]))
    return username


def register(connect):
    cursor = connect.cursor()
    first_name = get_input(cursor, 'first name', False, '')
    last_name = get_input(cursor, 'last name', False, '')
    username = get_input(cursor, 'username', True, 'username')
    password = get_input(cursor, 'password', False, '')
    email = get_input(cursor, 'email', True, 'email')
    now = date.today()
    cursor.execute("CALL addUser('{0}','{1}','{2}','{3}','{4}','{5}','{6}');".format(username, password, email, first_name, last_name, now.strftime('%Y-%m-%d'),now.strftime('%Y-%m-%d')))
    connect.commit()
    cursor.execute("SELECT user_id FROM users WHERE username='{0}';".format(username))
    user_id= cursor.fetchone()[0]
    print('(for testing) user id is:'+ str(user_id))
    print("Signup successful!")


def get_input(cursor, target, unique_check, row_to_check):
    while True:
        entered_input = input("Please enter " + target + ":")
        cleaned_input = entered_input.strip()
        if len(cleaned_input) == 0:
            print("Your " + target + " cannot be blank.")
            continue
        if unique_check:
            sql_str = "SELECT COUNT({0}) FROM users WHERE {1}='{2}';".format(row_to_check, row_to_check, cleaned_input)
            cursor.execute(sql_str)

            if cursor.fetchone()[0] != 0:
                print(cleaned_input + " is already taken.")
                continue
        break

    return cleaned_input


def quit_program(connect):
    print('program closes')
    connect.close()
    exit()
