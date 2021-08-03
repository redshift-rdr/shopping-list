from flask import Blueprint, request
from functions import validate_json

api = Blueprint('api', __name__, template_folder='templates')



@api.route('/api/lists/add', methods=['POST'])
def add_list():
    """ adds a new list

        @args (json):
            name -          the name of the list
    """
    # get the submitted json data
    post_json = request.json

    # check the posted data has required parameters
    validate_json(post_json, ['name'])


