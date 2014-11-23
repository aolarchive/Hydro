__author__ = 'yanivshalev'
from hydro.connectors.mysql import MySqlConnector

if __name__ == '__main__':
    params = {
        'source_type': 'mysql',
        'connection_type': 'connection_string',
        'connection_string': '127.0.0.1',
        'db_name': 'test',
        'db_user': 'xxx',
        'db_password': 'yyy'
    }
    con = MySqlConnector(params)
    print con.execute('select 1 a')
