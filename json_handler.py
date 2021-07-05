import json
import base64


def create_paring_request_message(client_name) :
    """
    This function will generate json string for ping request message
    :param client_name: get name of the client
    :return: json string of created message
    """

    message = {"protocol_version":1,"payload":{"service_name":"androidtvremote","client_name":client_name},"type":10,"status":200}
    json_dump = json.dumps(message)
    return json_dump

def create_option_message() :
    """
    This function will generate json string for option message
    :return: json string of created message
    """

    message = {"protocol_version":1,"payload":{"output_encodings":[{"symbol_length":4,"type":3}],
    "input_encodings":[{"symbol_length":4,"type":3}],"preferred_role":1},"type":20,"status":200}
    json_dump = json.dumps(message)
    return json_dump

def create_configuration_mesaage() :
    """
    This function will generate json string for configuration message
    :return: json string of created message
    """

    message = {"protocol_version":1,"payload":{"encoding":{"symbol_length":4,"type":3},"client_role":1},"type":30,"status":200}
    json_dump = json.dumps(message)
    return json_dump

def create_secret_message(secret_hash) :
    """
    This function will generate json string for secret message
    :param secret_hash: get string of clients secret hash
    :return: json string of created message
    """

    message = {"protocol_version":1,"payload":{"secret":base64.b64encode(secret_hash).decode()},"type":40,"status":200}
    json_dump = json.dumps(message)
    return json_dump

def parse_json_message(raw_data) :
    """
    This function will parse the json message
    :param raw_data: get bytes of raw json message 
    :return: extracted status and type of the message
    """

    json_object = json.loads(raw_data)
    message_status = json_object["status"]
    message_type = 0
    if message_status == 200 :
        message_type = json_object["type"]
    return message_status, message_type