import psycopg2
import os
from sshtunnel import SSHTunnelForwarder, BaseSSHTunnelForwarderError


def connect():
    with open('credentials.txt') as f:
        authenticator = [line.strip() for line in f]
        server = SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                                    ssh_username=authenticator[0],
                                    ssh_password=authenticator[1],
                                    remote_bind_address=('localhost', 5432))
        try:
            server.start()
        except (BaseSSHTunnelForwarderError):
            print("Error Connecting to SSH Tunnel")
            return 0

        params = {
            'database': 'p320_13',
            'user': authenticator[0],
            'password': authenticator[1],
            'host': 'localhost',
            'port': server.local_bind_port,
            'options': f'-c search_path=p320_13',
        }
        return psycopg2.connect(**params)


def exec_schema_file(path):
    full_path = os.path.join(os.path.dirname(__file__), f'{path}')
    conn = connect()
    if conn!=0 :
        cur = conn.cursor()
        with open(full_path, 'r') as file:
            cur.execute(file.read())
        conn.commit()

def exec_get_one(sql, args={}):
    conn = connect()
    if conn!=0 :
        cur = conn.cursor()
        cur.execute(sql, args)
        one = cur.fetchone()
        conn.close()
        return one
    else: 
        return


def exec_get_all(sql, args={}):
    conn = connect()
    if conn!=0 :
        cur = conn.cursor()
        cur.execute(sql, args)
        list_of_tuples = cur.fetchall()
        conn.close()
        return list_of_tuples
    else: 
        return


def exec_commit(sql, args={}):
    conn = connect()
    if conn!=0 :
        cur = conn.cursor()
        result = cur.execute(sql, args)
        conn.commit()
        conn.close()
        return result
    else: 
        return
