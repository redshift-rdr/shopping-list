import sqlite3, os, uuid
from typing import Any, Dict, List
from typing_extensions import Literal
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
        list_id | item_id | active | added
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

    # we set the row_factory on connection to get rows as dicts
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row

    return conn

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
        cursor : sqlite3.Cursor = get_cursor()
        retval : Any = function(cursor, *args, *kwargs)
        cursor.connection.commit()
        cursor.connection.close()
        return retval
    return wrapper

def rows_to_dicts(rows : List[sqlite3.Row]) -> List[dict]:
    """ takes the sqlite3.Row objects returned by cursor.fetchall() and
        turns them into dicts
    
        Parameters
        ----------
        rows : list, required
            A list of sqlite3.Row objects, returned from cursor.fetchall()
            Note that the connection object used by sqlite has been set to use
            a row_factory, which enables the conversion to dicts.
    """
    return [dict(row) for row in rows]

@db_access
def _create_list(cursor : sqlite3.Cursor) -> str:
    """ creates a list by adding it to the 'lists' table

        should not be called directly. use add_list

        Parameters
        ----------
        cursor : sqlite3.Cursor, required
            As long as this function is decorated with @db_access then
            the cursor will be passed automatically, and the connection
            closed when the function finishes.
    """
    id = uuid.uuid4().hex
    cursor.execute("INSERT INTO 'lists' VALUES(?, ?, ?)", (id, 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    return id

@db_access
def add_list(cursor : sqlite3.Cursor, add_recurring_items : bool = True) -> None:
    """ adds a new list to the application, auto adds recurring items

        Parameters
        ----------
        cursor : sqlite3.Cursor, required
            As long as this function is decorated with @db_access then
            the cursor will be passed automatically, and the connection
            closed when the function finishes.

        add_recurring_items : bool, optional
            if True, add recurring items to the list
    """
    list_id = _create_list()

    if add_recurring_items:
        item_list = get_recurring_items()
        for item in item_list:
            cursor.execute("INSERT INTO 'item_allocation' VALUES(?, ?, ?, ?)", (list_id, item['id'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1))

@db_access
def remove_list(cursor : sqlite3.Cursor, list_id : str) -> None:
    """ deletes an entry from the 'lists' table
    
        Parameters
        ----------
        cursor : sqlite3.Cursor, required
            As long as this function is decorated with @db_access then
            the cursor will be passed automatically, and the connection
            closed when the function finishes.

        list_id : str, required
            The UUID of the list to be deleted
    """
    assert(list_id)

    cursor.execute("DELETE FROM 'lists' WHERE id = ?", (list_id, ))

@db_access
def add_item(cursor : sqlite3.Cursor, list_id : str, name : str, img_path : str ='', recurring : int = 0) -> None:
    """ adds an item to the database, and links it with a list
    
        An item is linked to a list using the 'item_allocation' table.

        Parameters
        ----------
        cursor : sqlite3.Cursor, required
            As long as this function is decorated with @db_access then
            the cursor will be passed automatically, and the connection
            closed when the function finishes.

        list_id : str, required
            The UUID of the list the item is being added to

        name : str, required
            The name of the item being added

        img_path : str, optional
            The path to an image to be associated with the item

        recurring : int, optional
            This controls whether the item should be added to new lists
            when they are created
    """
    assert(all([list_id, name]))

    # create a uuid for the item
    item_uuid = uuid.uuid4().hex

    # sql statement to add item to the items table
    cursor.execute("INSERT INTO 'items' VALUES(?, ?, ?, ?)", (item_uuid, name, img_path, recurring))

    # sql statement to link the item with a list
    cursor.execute("INSERT INTO 'item_allocation' VALUES(?, ?, ?, ?)", (list_id, item_uuid, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1))

@db_access
def remove_item(cursor : sqlite3.Cursor, list_id : str, item_id : str) -> None:
    """ destroys the link between an item and a list, effectively removing the item from the list

        this does not remove the item from the database, the item is still accessible in the 'items' table.
    
        Parameters
        ----------
        cursor : sqlite3.Cursor, required
            As long as this function is decorated with @db_access then
            the cursor will be passed automatically, and the connection
            closed when the function finishes.

        list_id : str, required
            The UUID of the list the item is being removed from

        item_id : str, required
            The UUID of the item being removed
    """
    assert(all([list_id, item_id]))

    cursor.execute("DELETE FROM 'item_allocation' WHERE list_id = ? AND item_id = ?", (list_id, item_id))

@db_access
def get_list(cursor : sqlite3.Cursor, list_id : str) -> List[dict]:
    """ retrieves all items in a list 

        Parameters
        ----------
        cursor : sqlite3.Cursor, required
            As long as this function is decorated with @db_access then
            the cursor will be passed automatically, and the connection
            closed when the function finishes.

        list_id : str, required
            The UUID of the list to be retrieved
    """
    assert(list_id)

    cursor.execute("SELECT item_id, name, img, added, active FROM 'items' LEFT OUTER JOIN 'item_allocation' ON items.id = item_allocation.item_id WHERE item_allocation.list_id = ?", (list_id, ))
    
    # convert rows returned by sqlite to dicts
    return rows_to_dicts(cursor.fetchall())

@db_access
def get_items(cursor : sqlite3.Cursor, query : str = '') -> List[dict]:
    """ retrieves all items in the database, that begins with a query string

        Parameters
        ----------
        cursor : sqlite3.Cursor, required
            As long as this function is decorated with @db_access then
            the cursor will be passed automatically, and the connection
            closed when the function finishes.

        query : str, optional
            A search string that will filter results that begin with the string
    """
    cursor.execute("SELECT id, name, img, recurring FROM 'items' WHERE name LIKE ?", (f'{query}%', ))

    # convert rows returned by sqlite to dicts
    return rows_to_dicts(cursor.fetchall())

@db_access
def get_recurring_items(cursor : sqlite3.Cursor) -> List[dict]:
    """ retrieves all items in the database that have 'recurring' set to 1

        Parameters
        ----------
        cursor : sqlite3.Cursor, required
            As long as this function is decorated with @db_access then
            the cursor will be passed automatically, and the connection
            closed when the function finishes.
    """
    cursor.execute("SELECT id, name, img, recurring FROM 'items' WHERE recurring = 1")

    # convert rows returned by sqlite to dicts
    return rows_to_dicts(cursor.fetchall())

@db_access
def deativate_item(cursor : sqlite3.Cursor, list_id : str, item_id : str) -> None:
    """ 
    """
    pass