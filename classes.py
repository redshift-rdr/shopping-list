import sqlite3, os, uuid
import config
from datetime import datetime

"""
DB Structure
------------
    Tables
    ------
    lists
    items
    item_allocation

        lists
        -----
        id | active | created

        items
        -----
        id | name | img 

        item_allocation
        ---------------
        list_id | item_id | added
"""

def connect_to_db(path : str) -> sqlite3.Connection:
    """ creates a connection to a sqlite database

        if the db doesn't exist it will create one.

        Parameters
        ----------
        path : str, required
            The filesystem path to the sqlite database
    """
    # as the db path should come from the config file, if the db
    # doesn't exist then something is wrong
    assert os.path.exists(path)

    return sqlite3.connect(path)

def get_cursor() -> sqlite3.Cursor:
    """ creates a Cursor object used to interact with the database

        It will automatically create a connection to the database
    """
    return connect_to_db(config.DB_FILE_PATH).cursor()

def db_access(function):
    """ used to wrap functions that need database access

        It gets a reference to the db cursor, which the function can use
        without needing to creating one itself, and then closes the db
        connection when the function is done.
    
    """
    def wrapper(*args, **kwargs):
        cursor = get_cursor()
        function(cursor)
        cursor.connection.commit()
        cursor.connection.close()
    return wrapper

@db_access
def create_list(cursor : sqlite3.Cursor):
    """ adds an entry to the 'lists' table

        Parameters
        ----------
        cursor : sqlite3.Cursor, required
            As long as this function is decorated with @db_access then
            the cursor will be passed automatically, and the connection
            closed when the function finishes.
    """
    id = uuid.uuid4().hex
    cursor.execute("INSERT INTO 'lists' VALUES(?, ?, ?)", (id, 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))