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
        'show_stats': 'show_stats',
        'inspect_available_tools': 'inspect_available_tools',
        'inspect_lent_tools': 'inspect_lent_tools',
        'inspect_borrowed_tools': 'inspect_borrowed_tools'
    }
    return input_map


def show_stats(args):
    print('Action: Show Stats')
    print(args)


# The list of available tools must be ordered by name alphabetically
def inspect_available_tools(args):
    # REQ: 10 a
    print('Action: inspect_available_tools')
    tuples = exec_get_all('SELECT name FROM tools WHERE available is True ORDER BY name ASC;')
    [print(t[0]) for t in tuples]


def inspect_lent_tools(args):
    # REQ:10 b
    print('Action: inspect_lent_tools')

    tuples = exec_get_all(
        "SELECT r.tool_id, t.name, u.username as holder, r.overdue, r.date_borrowed,r.date_returned "
        "FROM user_tool_requests r "
        "Inner JOIN users u ON r.requesting_user_id= u.user_id "
        "INNER JOIN tools t on t.tool_id = r.tool_id "
        "WHERE r.status ='accepted' AND r.date_borrowed is not null "
        "ORDER BY r.date_borrowed ASC;")


    for tup in tuples:
        # if the tools hasn't been returned=> current holder is the borrower
        if tup[5]:
            current_holder = exec_get_one("SELECT u.username as owner FROM "
                                          "catalog_tools c INNER JOIN users u ON "
                                          "u.user_id= c.owner_id WHERE c.tool_id={0};".format(tup[0]))[0]
        else:  # If the tools is returned, current holder is its borrower
            current_holder = tup[2]
        print(
            "Tool id:{0} | current holder:{1} | overdue:{2} | date borrowed:{3} ".format(tup[0], current_holder,
                                                                             str(tup[3]),
                                                                             str(tup[4])))


def inspect_borrowed_tools(args):
    # REQ:10 c
    print('Action: inspect_borrowed_tools')
    tuples = exec_get_all("SELECT r.tool_id, t.name, u.username as tool_owner, r.overdue, r.date_borrowed "
                          "FROM user_tool_requests r "
                          "INNER JOIN catalog_tools c ON r.tool_id=c.tool_id "
                          "INNER JOIN users u ON c.owner_id=u.user_id "
                          "INNER JOIN tools t on t.tool_id = r.tool_id "
                          "WHERE r.status='accepted' AND r.date_borrowed is not null "
                          "ORDER BY r.date_borrowed ASC;")
    [print("Tool id:{0} | owner:{1} | overdue:{2} | date borrowed:{3} ".format(t[0], t[2], str(t[3]), str(t[4]))) for t in
     tuples]
