import re
from pluto_api.exceptions import AppError

"""
Path to Solution
1. Analyze the Problem
    1. Analyze the input template given by Pluto
    2. Recognize these patterns 
        - !variable=value is used for variable declaration
        - !<varible> accepts input until the end of the line
        - @variable is used for variable interpolation
        - @ symbols are escaped with a single @ 
        - @{variable}<text> is used for concatention
    3. The notes suggest that the input may not compile correctly
        - Errors are not explicitly stated nor is an example of a template that would not compile given,
            thus we will make the following assumption for a correctly compiled template
                1. !<variable> is exclusively reserved for variable declaration
                        - must not be immediately preceded by an ! and must be immediately followed by a =<value> token
                2. an odd number of @ symbols must be followed by a declared varible
                3. @variable<text> will not be recognized as a valid interpolation
                    - deemed undeclared variable
2. Break down the problem into smaller steps
    - Look for compile errors
    - Look for variable declarations
    - use a helper function with a stack to parse nested variable values
    - remove variable declarations
    - resolve escaped character and variables
    - look for lingering errors

NOTE: I could have used Jinja2 for this but not sure if that was allowed
so I implemented a near bare bones solution.
"""


class Stack:
    def __init__(self):
        self.li = []
        self.length = 0

    def push(self, x):
        self.li.append(x)
        self.length += 1

    def pop(self):
        term = ''
        if self.length != 0:
            term = self.li.pop()
            self.length -= 1
        return term


def resolve_variable(value: str, mapping: dict):
    """ Resolve all tokens in the input string to terminals """

    # there is no var declaration here so we simply return the string
    if "@" not in value:
        return value

    # create a collection of terminals that we may accept
    non_terminals = [f"@{key}" for key in mapping]
    # regex to search for all terminals
    pattern = "|".join(non_terminals)
    # tokenize the string
    tokens = value.split()

    # create a Stack as an efficient ds for parsing
    s = Stack()
    # push all tokens on the stack
    for token in tokens:
        s.push(token)

    # the value to be returned
    new_value = []
    while s.length:
        # get token from the stack
        term = s.pop()
        # if token is an accepted non-terminal
        token_found = re.search(pattern, term)
        if token_found:
            # we are going to resolve that non-terminal and
            # push it into the stack
            var = token_found.group()
            new_term = re.sub(var, mapping[var[1:]], term)
            new_term = new_term.split()
            for nt in new_term:
                s.push(nt)
        else:
            # we found a terminal token so we will add it
            # to our new value
            new_value.append(term)

    # we need to order our value correctly and turn it into a str
    new_value = " ".join(new_value[::-1])
    # check if there are any undefined variables
    if re.search("@\w+", new_value):
        raise AppError("undefined variable", 400)
    return new_value.strip()


def template_formatter(template: str):
    """ 
        Format a Pluto template as plain text

        Accepts:
            - template: text from a Pluto template
        Return
            - formatted: text formatted as plain text with
                all variables
    """

    # first we want to parse the template for our error cases
    # look for malformed declared variables
    # preceded by an !
    error = bool(re.findall(r"!(!\w+)=(.*?)", template))
    # not followed by =<value>
    error = error or bool(re.findall(r"(!\w+)\s*?=?\s+(\S+)", template))
    if error:
        raise AppError("bad variable declaration", 400)

    # look for odd multiple of @ not followed by a printable characters(possible var)
    error = re.search(r"[^@]@(@@)*\s+", template)
    if error:
        raise AppError("bad interpolation", 400)

    # here we begin parsing our template
    # use regular expression to parse variables from template
    parsed_var_regex = r"(!\w+?)=([(@?\w)\- \.]+)\n"
    parsed_variables = re.findall(parsed_var_regex, template)
    # create a mapping for template variables to their values
    template_variables = {f"{var[0][1:]}": var[1].strip()
                          for var in parsed_variables}

    # we need to ensure that we have resolved all non-terminals
    for template_var in template_variables:
        template_variables[template_var] = resolve_variable(
            template_variables[template_var],
            template_variables
        )

    # transform to a list for variable resolution
    template_variables = list(template_variables.items())

    # now we want to resolve each deliberate @ token and remove variable declaration
    formatted = re.sub(r"(@@)", "@", template)
    formatted = re.sub(parsed_var_regex, "", formatted)

    # replace each variable in our template with its value
    for var in template_variables:
        pattern = f"@{var[0]}"
        formatted = re.sub(pattern, var[1], formatted)
        pattern = "@{" + var[0] + "}"
        formatted = re.sub(pattern, var[1], formatted)

    # now we can complete our error checking to see
    # if there are any remaining reserved token
    # we may have undefined variables and so we throw an error
    # here we are looking for the concatention token
    error = re.search("@{\w+", formatted)
    # here we are looking for the interpolation token
    # any token beginning with a non-printable char, @ and ending a non-printable
    error = error or re.search(r"[\s]+(@?@)\w+[\s]+", formatted)
    if error:
        raise AppError("undefined variable", 400)
    return formatted.strip()
