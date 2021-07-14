# Default Azure Imports
import logging
import azure.functions as func
# Imports for Python script that are outside Azure
import ast
import operator as op
import json

# Constants
# Supported Operators
OPERATORS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg}
# Request Parameters/JSON Keys
CALCULATE_PARAM = 'calculate'

def main(req: func.HttpRequest) -> func.HttpResponse:
    expression_to_calculate = extract_any_param(req, CALCULATE_PARAM, None)
    logging.info(f'Expression: {expression_to_calculate}')

    if expression_to_calculate is not None and len(expression_to_calculate) > 0:
        result_json = {
            'expression': expression_to_calculate,
            'result': eval_expr(expression_to_calculate)
        }
        return func.HttpResponse(json.dumps(result_json), mimetype='application/json')
    else:
        return func.HttpResponse(
             "ERROR: You must supply a calculate parameter to perform calculations",
             status_code=400
        )


def eval_expr(expr):
    """
    Evaluates String mathematical expression to produce a result
    """
    return eval_(ast.parse(expr, mode='eval').body)

def eval_(node):
    if isinstance(node, ast.Num): # <number>
        return node.n
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        return OPERATORS[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        return OPERATORS[type(node.op)](eval_(node.operand))
    else:
        raise TypeError(node)

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
    logging.info(f'PARAM: {result_param}')
    return default_value if result_param is None else result_param
