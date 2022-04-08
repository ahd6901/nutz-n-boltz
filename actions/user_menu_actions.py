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
        'display_dashboard': 'display_dashboard',
        'show_stats': 'show_stats',
        'inspect_available_tools': 'inspect_available_tools',
        'inspect_lent_tools': 'inspect_lent_tools',
        'inspect_borrowed_tools': 'inspect_borrowed_tools'
    }
    return input_map


def show_stats(args, userid):
    #testing user: Sn4ppy_dozerSambur
    print('Action: Show Stats')
    print("===Your top 10 most frequently lent tools and each's average lent time:")
    ten_most_lent = exec_get_all("SELECT t.tool_id, t.name,count(r.tool_id) FROM user_tool_requests r "
                                 "INNER JOIN catalog_tools c on r.tool_id = c.tool_id "
                                 "INNER JOIN tools t on t.tool_id = r.tool_id "
                                 "WHERE c.owner_id={0} and r.status='accepted' "
                                 "GROUP BY t.tool_id "
                                 "ORDER BY COUNT(r.tool_id) DESC "
                                 "LIMIT 10;".format(userid))
    if len(ten_most_lent) == 0:
        print("You haven't lent any tools")
    else:
        for t in ten_most_lent:
            avg_lent_time = exec_get_one(
                "SELECT avg(num_days) FROM "
                "("
                " SELECT (r.expected_return_date-r.date_required) as num_days FROM user_tool_requests r "
                " WHERE r.tool_id={0} AND r.status='accepted'"
                ")"
                "as new_col;".format(t[0]))
            print('tool id:', t[0], ', ', 'tool name:', t[1], ', Average lent time:', int(avg_lent_time[0]), 'days')

    borrowed_count_tuples = exec_get_all("SELECT r.tool_id, t.name, COUNT(r.tool_id) FROM user_tool_requests r "
                                         "INNER JOIN tools t on t.tool_id = r.tool_id WHERE r.requesting_user_id={0} "
                                         "GROUP BY r.tool_id, t.name ORDER BY COUNT(r.tool_id) DESC LIMIT 10;".format(
        userid))
    print('===Your top 10 most frequently borrowed tools:')
    if len(borrowed_count_tuples) == 0:
        print("You haven't borrowed any tools")
    else:
        [print('tool id:', t[0], ' ', 'name:', t[1]) for t in borrowed_count_tuples]


def display_dashboard(args, userid):
    print('Action: display_dashboard')
    count_available = exec_get_one(
        'SELECT COUNT(t.tool_id) '
        'FROM tools t INNER JOIN catalog_tools c ON t.tool_id = c.tool_id '
        'WHERE t.available is True AND c.owner_id={0};'.format(userid))
    print("Number of tools available from your catalog:", count_available[0])
    count_lent = exec_get_one("SELECT count(distinct(r.tool_id)) "
                              "FROM user_tool_requests r JOIN catalog_tools c on r.tool_id = c.tool_id "
                              "WHERE c.owner_id={0} AND r.status ='accepted';".format(userid))
    print('Number tools you have lent:', count_lent[0])

    count_borrowed = exec_get_one("SELECT COUNT(DISTINCT(r.tool_id)) "
                                  "FROM user_tool_requests r "
                                  "WHERE r.requesting_user_id={0} AND r.status ='accepted' ;".format(
        userid))
    print('Number tools you have borrowed:', count_borrowed[0])


def inspect_available_tools(args, userid):
    # REQ: 10 a
    print('Action: inspect_available_tools')
    tuples = exec_get_all('SELECT name FROM tools WHERE available is True ORDER BY name ASC;')
    [print(t[0]) for t in tuples]


def inspect_lent_tools(args, userid):
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


def inspect_borrowed_tools(args, userid):
    # REQ:10 c
    print('Action: inspect_borrowed_tools')
    tuples = exec_get_all("SELECT r.tool_id, t.name, u.username as tool_owner, r.overdue, r.date_borrowed "
                          "FROM user_tool_requests r "
                          "INNER JOIN catalog_tools c ON r.tool_id=c.tool_id "
                          "INNER JOIN users u ON c.owner_id=u.user_id "
                          "INNER JOIN tools t on t.tool_id = r.tool_id "
                          "WHERE r.status='accepted' AND r.date_borrowed is not null "
                          "ORDER BY r.date_borrowed ASC;")
    [print("Tool id:{0} | owner:{1} | overdue:{2} | date borrowed:{3} ".format(t[0], t[2], str(t[3]), str(t[4]))) for t
     in
     tuples]
