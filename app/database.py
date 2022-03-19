# Some of this file is based on code in the flask documentation
# specifically, examples in the following places
# - https://flask.palletsprojects.com/en/2.0.x/appcontext/
# - https://flask.palletsprojects.com/en/2.0.x/reqcontext/
# - https://flask.palletsprojects.com/en/2.0.x/api/#flask.Flask.before_request
# Accessed Thu 03 Mar 2022

import mariadb as db
from flask import current_app, g

DB_CONNECTION_KEY = 'db_connection'

def connect():
    config = current_app.config
    if config['DB_UNIX_SOCKET'] is not None:        
        return db.connect(
            unix_socket=config['DB_UNIX_SOCKET'],
            user=config['DB_USER'],
            password=config['DB_PASSWORD'],
            database=config['DB_DATABASE'])
    else:
        return db.connect(
            host=config['DB_HOST'],
            port=config['DB_PORT'],
            user=config['DB_USER'],
            password=config['DB_PASSWORD'],
            database=config['DB_DATABASE'])

def get_connection():
    if not DB_CONNECTION_KEY in g:
        return g.setdefault(DB_CONNECTION_KEY, connect())
    else:
        return g.get(DB_CONNECTION_KEY)

def execute(query, *args):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(query, tuple(args))
    return cursor

def rollback():
    connection = g.pop(DB_CONNECTION_KEY, None)
    if connection is not None:
        connection.rollback()
    
def close_connection(err=None):
    connection = g.pop(DB_CONNECTION_KEY, None)
    if connection is not None:
        connection.commit()
        connection.close()

def escape_string(string):
    return get_connection().escape_string(string)
