import db
from flask import Blueprint, request, jsonify
from functions import validate_json

api = Blueprint('api', __name__, template_folder='templates')

@api.route('/api/lists/add', methods=['GET'])
def add_list():
    """ adds a new list

        This function does not require any input, it simply creates a list and returns
        the list ID.

        Parameters
        ----------
        none

        Returns
        -------
        200 - {"message" : "list added successfully"}
            List was added

        500 - {"message" : "there was a problem"}
            The list was not able to be added due to an unforeseen problem
    """
    status = db.add_list()

    if status == db.DB_STATUS.ERROR:
        return jsonify({"message": "there was a problem"}), 500
    elif status == db.DB_STATUS.SUCCESS:
        return jsonify({"message": "list added successfully"})

@api.route('/api/lists/retire', methods=['POST'])
def retire_list():
    """ retires (or deactivates) a list, sending it to the 'previous list' section

        Parameters
        ----------
        list_id : str, required

        Returns
        -------
        200 - 
            The list was retired successfully

        400 - 
            The list could not be found

        500 -
            There was an unexpected error
    """
    post_json = request.json
    if not validate_json(post_json, ['list_id']):
        return jsonify({'message': 'required parameter not provided'}), 400

    status = db.deactivate_list(post_json['list_id'])

    # need to add a new list or there wont be any current list
    db.add_list()
    
    if status == db.DB_STATUS.ERROR:
        return jsonify({'message': 'there was an error'}), 500
    elif status == db.DB_STATUS.SUCCESS:
        return jsonify({'message': 'list retired successfully'})

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
        200 - {"message" : "item added successfully"}
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
    post_json = request.json
    if not validate_json(post_json, ['list_id', 'name']):
        return jsonify({'message': 'required parameter not provided'}), 400

    # check the list is in the database
    if not db.list_exists(post_json['list_id']):
        return jsonify({'message': 'list could not be found'}), 404

    # check the name complies with the rules
    if len(post_json['name']) > 30 and post_json['name'].isalnum():
        return jsonify({'message': 'invalid item name'}), 400

    status = db.add_item(post_json['list_id'], post_json['name'])
    if status == db.DB_STATUS.ERROR:
        return jsonify({'message': 'there was an error'}), 500
    elif status == db.DB_STATUS.SUCCESS:
        return jsonify({'message': 'item added successfully'})

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
    post_json = request.json
    if not validate_json(post_json, ['list_id', 'item_id']):
        return jsonify({'message': 'required parameter not provided'}), 400

    # check the list is in the database
    if not db.list_exists(post_json['list_id']):
        return jsonify({'message': 'list could not be found'}), 404

    status = db.remove_item(post_json['list_id'], post_json['item_id'])
    if status == db.DB_STATUS.ERROR:
        return jsonify({'message': 'there was an error'}), 500
    elif status == db.DB_STATUS.SUCCESS:
        return jsonify({'message': 'item removed successfully'})

@api.route('/api/items/make_recurring', methods=['POST'])
def make_recurring_item():
    """ makes an item recurring, meaning it is automatically included in new lists

        Parameters (json)
        -----------------
        item_id : str, required
            The UUID of the item that is to be recurring

        Returns
        -------
        200 - {"message" : "item made recurring successfully"}
            The item was made recurring

        400 - {"message" : "required parameter not provided"}
            list_id or item_id not provided

        404 - {"message" : "item not found"}
            item_id could not be found in the database

        500 - {"message" : "there was an error"}
            There was a database error
    """ 
    post_json = request.json
    if not validate_json(post_json, ['item_id']):
        return jsonify({'message': 'required parameter not provided'}), 400

    status : db.DB_STATUS = db.update_recurring_item(post_json['item_id'], 1)
    if status == db.DB_STATUS.ERROR:
        return jsonify({'message': 'there was an error'}), 500
    elif status == db.DB_STATUS.SUCCESS:
        return jsonify({'message': 'item made recurring successfully'})

@api.route('/api/items/get', methods=['POST'])
def get_matching_items():
    """ fetches items that start with a provided string

        this provides a list of items that are already in the 
        database

        Parameters (json)
        -----------------
        match_string : str, required
            The string that will be matched in the database, so if a string of
            'stra' is provided it will return 'strawberries', 'straight bananas', 'straws'

        Returns
        -------
        200 - {['strawberries', 'straws']}
            A list of items matching the provided string

        400 - {"message" : "required parameter not provided"}
            list_id or item_id not provided

        400 - {"message" : "invalid parameter"}
            One of the parameters was invalid
    """
    post_json : dict = request.json
    if not validate_json(post_json, ['match_string']):
        return jsonify({'message': 'required parameter not provided'}), 400

    if post_json['match_string']:
        items : list = db.get_items(post_json['match_string'])
        items = [item['name'] for item in items]
    else:
        items = []

    return jsonify(items)