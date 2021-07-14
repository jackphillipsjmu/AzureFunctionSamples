# Default Azure Imports
import logging
import azure.functions as func
# Imports for Python script that are outside Azure
from PIL import Image
import io
import zipfile
from datetime import datetime
import pathlib
from distutils.util import strtobool
import re

# Constants
DEFAULT_IMG_NAME = 'default_img.png'
DEFAULT_IMG_NAME_PARAM = 'default_image_name'
INCLUDE_TIMESTAMP_PARAM = 'include_timestamp'

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """
    Takes in a request, parses out the image data and then creates an in-memory
    zip file representation that is provided in the response.
    """
    # Pull in either Request Params or Form Request Variables from the request
    # and store them in variables.
    # The first will read in the include_timestamp parameter if it exists and then parse it
    # to a boolean.
    include_timestamp = parse_to_bool(extract_any_param(req, INCLUDE_TIMESTAMP_PARAM, 'F'))
    # Next, we'll get an overridden default file name if we cannot determine the file name
    # ourselves this can be used when binary data is submitted to the function.
    default_file_name = extract_any_param(req, DEFAULT_IMG_NAME_PARAM, DEFAULT_IMG_NAME)
    logging.info(f'Default File Name: {default_file_name}')
    logging.info(f'Include Timestamp: {include_timestamp}')

    result_files = []
    image_dict = get_images(req, default_file_name, include_timestamp)
    # If we have a valid image dictionary of file names -> Image then process them
    if len(image_dict) > 0:
        logging.info('Files Found!')
        for file_name, image in image_dict.items():
            logging.info(f'Processing File {file_name}')
            result = convert_to_grayscale(image, context)
            result_files.append((file_name, result))
    # Ensure we have images to process
    # if not, then return an HTTP 400 error
    if len(result_files) > 0:
        logging.info('Generating Zip File In Memory')
        full_zip_in_memory = generate_zip(result_files)
        return func.HttpResponse(full_zip_in_memory)
    else:
        return func.HttpResponse(f'No Valid Files Provided to be Processed!', status_code=400)

def parse_to_bool(param: str, default_value: bool = False) -> bool:
    """
    Parses the param string to a boolean value if possible.

    True values are y, yes, t, true, on and 1;
    false values are n, no, f, false, off and 0.
    Raises ValueError if val is anything else.
    """
    # Strip out non-alpha characters
    if param is None:
        logging.info('No parameter provided!')
        return default_value
    alpha_string = re.sub(r'\W+', '', param)
    return bool(strtobool(alpha_string))

def generate_zip(files):
    """
    Creates an in-memory zip file from the list of tuple (filename, image data)
    """
    mem_zip = io.BytesIO()

    with zipfile.ZipFile(mem_zip, mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.writestr(f[0], f[1])

    return mem_zip.getvalue()

def get_images(req: func.HttpRequest, default_file_name: str = DEFAULT_IMG_NAME, apply_timestamp_to_output_file: bool = True):
    """
    Retrieves image either data supplied in a URL form encoded file(s) or single request body that uses binary data.
    """
    result_images = {}
    # If we have files in the request then this is an octet-stream/multipart form so process it accordingly.
    # Otherwise, we have a request body with an image supplied into it
    if len(req.files) > 0:
        logging.info(f'Files found! Number of files {len(req.files)}')
        for input_file in req.files.values():
            filename = append_timestamp_to_filename(input_file.filename) if apply_timestamp_to_output_file else input_file.filename
            image = Image.open(input_file)
            result_images[filename] = image
    else:
        logging.info(f'Retrieving File from Request Body')
        image_body = req.get_body()
        image = Image.open(io.BytesIO(image_body))
        default_file_name = append_timestamp_to_filename(default_file_name) if apply_timestamp_to_output_file else default_file_name
        result_images[default_file_name] = image

    return result_images

def append_timestamp_to_filename(filename: str) -> str:
    """
    Appends the current timestamp in yyyyMMdd-HHmmss format to the filename.
    So, foo.png would return foo-20210714-153329.png
    """
    file_path = pathlib.Path(filename)
    return f'{file_path.stem}-{datetime.now().strftime("%Y%m%d-%H%M%S")}{file_path.suffix}'

def extract_form_parameter(req: func.HttpRequest, form_parameter: str, default_value = None):
    """
    Inspects form parameters and attempts to retrieve it if it exists.
    """
    # Pull out form which is a ImmutableMultiDict if we have the parameter
    if form_parameter in req.form.to_dict().keys():
        logging.info(f'Form Parameter {form_parameter} found!')
        return req.form[form_parameter]
    # Return default_value if we do not have a supporting Form parameter
    return default_value

def extract_param(req: func.HttpRequest, parameter: str, default_value = None):
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

def extract_any_param(req: func.HttpRequest, parameter: str, default_value = None):
    """
    Inspects form parameters to see if the request parameter exists, if it does not it will
    then attempt to retrieve the request parameter. If all of these fails then the defaul value is returned
    """
    result_param = extract_form_parameter(req, parameter, None)
    if result_param is None:
        result_param = extract_param(req, parameter, None)
    return default_value if result_param is None else result_param

def convert_to_grayscale(image, context):
    """
    Converts an image to Grayscale and returns a byte array value
    """
    # Store inferred image as in memory byte array
    img_byte_arr = io.BytesIO()
    # Convert composite to LA grayscale so we can return a PNG
    image.convert('LA').save(img_byte_arr, format='png')
    final_image = img_byte_arr.getvalue()

    return final_image
