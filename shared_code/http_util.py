# Default Azure Imports
import logging
import azure.functions as func
import urllib.parse


def extract_form_parameter(req: func.HttpRequest, form_parameter: str, default_value=None):
    """
    Inspects form parameters and attempts to retrieve it if it exists.
    """
    # Pull out form which is a ImmutableMultiDict if we have the parameter
    if form_parameter in req.form.to_dict().keys():
        logging.info(f'Form Parameter {form_parameter} found!')
        return req.form[form_parameter]
    # Return default_value if we do not have a supporting Form parameter
    return default_value


def extract_param(req: func.HttpRequest, parameter: str, default_value=None):
    """
    Inspects request parameters and attempts to retrieve it if it exists.
    """
    result = req.params.get(parameter)
    if not result:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            result = req_body.get(parameter)
    return result if result else default_value


def extract_any_param(req: func.HttpRequest, parameter: str, default_value=None):
    """
    Inspects form parameters to see if the request parameter exists, if it does not it will
    then attempt to retrieve the request parameter. If all of these fails then the defaul value is returned
    """
    result_param = extract_form_parameter(req, parameter, None)
    if result_param is None:
        result_param = extract_param(req, parameter, None)
    return default_value if result_param is None else result_param


def print_http_request_info(req: func.HttpRequest):
    if req is not None:
        print(f'URL: {req.url}')
        print(f'Method: {req.method}')
        headers = {}
        for key, value in req.headers.items():
            headers[key] = value
        print(f'Headers: {headers}')
        print(f'Form: {req.form}')
        print(f'Params: {req.params}')
        print(f'Route Params: {req.route_params}')
        print(f'Body: {urllib.parse.unquote(req.get_body().decode("utf-8"))}')
    else:
        print('No HTTP Request Provided! Cannot print information.')


def decode_bytes_to_string(bytes_to_decode: bytes, encoding: str = 'utf-8'):
    return urllib.parse.unquote(bytes_to_decode.decode(encoding=encoding))


def encode_string(string, encoding: str = 'utf-8'):
    return urllib.parse.quote(string, encoding=encoding)


def encode_string_to_bytes(string, encoding: str = 'utf-8'):
    return bytes(urllib.parse.quote(string, encoding=encoding), encoding)


def build_form_request_body(key_value_pairs: dict):
    if key_value_pairs is None:
        raise ValueError('Cannot Build Request Body Without a Dictionary')

    result = ''
    size = len(key_value_pairs)
    count = 1
    for key, value in key_value_pairs.items():
        result += f'{key}={encode_string(value)}'
        if count != size:
            result += '&'
        count += 1
    return bytes(result, 'utf-8')
