import logging
import os
import re

def load_input_file(filename):
    logging.info("Loading input from file '{}'.".format(filename))
    k = os.path.basename(filename).split(".")[0]
    i = open(filename, "r")
    input_file_data = i.read()
    i.close()

    return input_file_data

def count_leading_spaces(line):
    return len(line) - len(line.lstrip(' '))

def start_zip_block(line):
    return line.lstrip().startswith("ZipFile:")

def valid_code(line):
    return not line.lstrip().startswith("-")

def replace_values_in_line(line, values):
    regex = re.match( r'^(.*)\${(.*?)}(.*)$', line)

    # If the line does not include any values, return it unchanged
    if regex == None:
        return line

    value_name = regex.group(2)

    if value_name not in values.keys():
        msg = "Value '{}' not provided.".format(value_name)
        logging.error(msg)
        raise Exception(msg)

    val = values.get(value_name)
    logging.info("Replacing cfn value '{}' with '{}'.".format(value_name, val))

    # !! Currently asssumes all values are strings !!
    modified_line = regex.group(1) + str(val) + regex.group(3)

    # Recur until no more variables match
    return replace_values_in_line(modified_line, values)

def replace_values(code, values):
    updated_code = {}
    for fn_name, fn_code in code.items():
        updated_code[fn_name] = [replace_values_in_line(l, values) for l in fn_code]
    return updated_code

def format_python_code(code):
    modified_code = {}
    for k, v in code.items():
        if len(v) == 0:
            logging.debug("Removing empty function '{}'.".format(k))
            continue

        logging.debug("Formatting function '{}'.".format(k))
        modified_fn = []

        num_spaces_function_indented = count_leading_spaces(v[0])
        logging.debug("Function indented {} spaces.".format(num_spaces_function_indented))

        logging.debug("Removing leading {} from every line.".format(num_spaces_function_indented))
        modified_code[k] = [line[num_spaces_function_indented:] for line in v]
    return modified_code

def is_comment(line):
    return line.strip().startswith("#")

def in_function_block(fn_significant_white_space):
    return fn_significant_white_space != 0

def load_functions_from_resource_data(resource_data):
    logging.debug("Loading functions from from resources.")

    # Set fn_significant_white_space to 0 to denote we are outside of a function body
    fn_significant_white_space = 0

    code = {}
    function_id = 0
    for line in resource_data:
        logging.debug("Evaluating line {}".format(line))

        if start_zip_block(line) and not in_function_block(fn_significant_white_space):
            logging.debug("Found line starting ZipFile block. Starting new function body with id {}.".format(function_id))
            fn_significant_white_space = count_leading_spaces(line)
            code[str(function_id)] = []
            continue

        if is_comment(line):
            logging.debug("Skipping comment.")
            continue

        if not line.strip():
            logging.debug("Skipping whitespace line.")
            continue

        if in_function_block(fn_significant_white_space) and not valid_code(line):
            logging.debug("YAML or invalid code in function body, skipping.".format(line))
            continue

        if in_function_block(fn_significant_white_space) and fn_significant_white_space <= count_leading_spaces(line):
            logging.debug("Valid code in function body, appending line to function.")
            code[str(function_id)].append(line)
            continue

        # If in the function body, and not handled by one of the above, assume end of function
        if in_function_block(fn_significant_white_space):
            logging.debug("End of function {}.".format(function_id))
            function_id += 1 # increment function_id to start the next function block
            fn_significant_white_space = 0 # set fn_significant_white_space to 0 to signify end of fn block
            continue

        logging.debug("Ignoring line outside function body.")

    logging.info("Done loading functions. Loaded {} function(s).".format(len(code)))

    return code

def load_resources(cfn_data):
    logging.debug("Loading resources from template.")
    result = []
    in_resources = False
    for line in cfn_data.split("\n"):
        logging.debug("Evaluation of line as resource {}".format(line))

        if is_comment(line):
            logging.debug("Skipping comment.")
            continue

        if not line.strip():
            logging.debug("Skipping whitespace line.")
            continue

        if line.startswith("Resources"):
            logging.debug("Found line starting Resources block.")
            in_resources = True
            continue

        if in_resources and count_leading_spaces(line) > 0:
            logging.debug("Appending line to resource block.")
            result.append(line)
            continue

        if in_resources:
            logging.debug("Found end of Resources block.")
            logging.debug("Done loading resources from template")
            return result

        logging.debug("Not taking any action on line.")

    if in_resources:
        logging.debug("Found EOF while in resources, returning resources as result.")
        return result

    # If falls all the way through without finding resources, throw exception
    raise Exception("No Resources in template.")

def convert_fns_to_str(fns):
    return {k: "\n".join(v) for (k, v) in fns.items()}

def extract_functions(cfn_data, values, convert_cfn_variables=True):
    resource_data = load_resources(cfn_data)
    fns = load_functions_from_resource_data(resource_data)
    modified_fns = format_python_code(fns)
    replaced_values = replace_values(modified_fns, values)
    return convert_fns_to_str(replaced_values)

def parse_csv_input_values(input_values):
    logging.debug("Paring input '{}'.".format(input_values))
    result = {}

    if input_values != "":
        result = {x[0]: x[1] for x in [v.split("=") for v in input_values.split(",")]}

    logging.debug("Parsed following values '{}'.".format(result))
    return result
