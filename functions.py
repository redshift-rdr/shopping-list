import json

def validate_json(json_data, required_params):
    """ validates that submitted json data contains the required parameters

        @args:
            json_data : dict -          json data received from client
            required_params : list -    a list of strings that are parameter names

        @returns:
            bool -                      true - all required parameters are present in json_data
                                        false - there are required parameters missing
    """
    return all([param in json_data for param in required_params])