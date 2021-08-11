import json, os, datetime
from typing import List, Dict, Any
import config

def log(message: str, path : str = config.LOG_FILE_PATH) -> None:
    """ writes application messages to a log file

        the message will be written to 'logs/application.log'. the current
        date and time will be added as a prefix to the message.

        Parameters
        ----------     
        message : str, required
            The message to be written to the log file

        path : str, required
            The path to the log file
    """
    with open(path, 'a+') as f:
        f.write(f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] - {message}\n')
    

def load_json(path: str) -> Dict[str, Any] or None:
    """ loads json data from a file and returns it

        Parameters
        ----------
        path : str, required
            the path to the file containing json data

        Raises
        ------
        FileNotFoundError
            If the file specified in 'path' doesn't exist
    """
    if not os.path.exists(path):
        log(f'[ERROR] functions.load_json {path} doesnt exist')
        return None

    loaded_json : Dict[str, Any]
    try:
        with open(path, 'r') as f:
            loaded_json = json.load(f)
    except json.decoder.JSONDecodeError:
        log(f'[ERROR] functions.load_json {path} is not a json file')
        return None

    return loaded_json

def validate_json(json_data: Dict[str, Any], required_params: List[str]) -> bool:
    """ validates that submitted json data contains the required parameters

        Parameters
        ----------
        json_data : dict, required
            json data received from client

        required_params : list[str], required
            a list of parameter names that should be in 'json_data'
    """
    return all([param in json_data for param in required_params])