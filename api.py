from flask import Blueprint, request
from functions import validate_json

api = Blueprint('api', __name__, template_folder='templates')



@api.route('/api/lists/add', methods=['GET'])
def add_list():
    """ adds a new list

        This function does not require any input, it simply creates a list and returns
        the list ID.
    """
    pass

@api.route('/api/lists/remove', methods=['POST'])
def remove_list():
    """ removes a list

        This function takes a list ID, and removes it. 

        Parameters
        ----------
        list_id : str, required
            The UUID of the list being removed

        Returns
        -------
        200 - {"message" : "list deleted successfully"}
            The list was deleted

        400 - {"message" : "required parameter not provided"}
            The list_id was not provided

        404 - {"message" : "list could not be found"}
            The list could not be found

        Example
        -------
        {
            "list_id" : "16fd2706-8baf-433b-82eb-8c7fada847da"
        }
    """
    post_json = request.json

    validate_json(post_json, ['list_id'])

    pass

@api.route('/api/items/add', methods=['POST'])
def add_item():
    """ adds an item to a list

        Parameters (json)
        -----------------
        list_id : str, required
            The UUID of the list the item is being added to

        name : str, required
            The name of the item

        Returns
        -------
        200 - {"message" : "item added successfully", "item_id" : "77fd2706-8baf-432b-82eb-8c7fada848jh"}
            The item was added to the list

        400 - {"message" : "required parameter not provided"}
            list_id or name not provided

        400 - {"message" : "invalid item name"}
            the item name needs to be alphanumeric characters, 1-30 characters long

        404 - {"message" : "list could not be found"}
            the list could not be found using the list_id provided

        Example
        -------
        {
            "list_id" : "16fd2706-8baf-433b-82eb-8c7fada847da",
            "name" : "Strawberries"
        }
    """
    pass

@api.route('/api/items/remove', methods=['POST'])
def remove_item():
    """ removes an item from a list

        Parameters (json)
        -----------------
        list_id : str, required
            The UUID of the list that the item is being removed from

        item_id : str, required
            The UUID of the item that is being removed

        Returns
        -------
        200 - {"message" : "item removed successfully"}
            The item was removed

        400 - {"message" : "required parameter not provided"}
            list_id or item_id not provided

        400 - {"message" : "invalid parameter"}
            One of the parameters was invalid

        404 - {"message" : "list or item not found"}
            Either list_id or item_id could not be found in the database
    """ 
    pass


