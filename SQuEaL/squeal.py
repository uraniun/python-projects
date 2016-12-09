import re
import itertools
from reading import *
from database import *

# Below, write:
# *The cartesian_product function
# *All other functions and helper functions
# *Main code that obtains queries from the keyboard,
#  processes them, and uses the below function to output csv results

def cartesian_product(first_table, second_table):
    """
    Generating cartesian product of two tables
    :param first_table:
    :param second_table:
    :return: new table with product
    """
    table_input_dict = {}
    first_table_rows = first_table.get_rows()
    second_table_rows = second_table.get_rows()
    product = [item for item in itertools.product(first_table_rows, second_table_rows)]  # using itertools generate product
    new_table_headers = first_table.get_column_names()
    new_table_headers.extend(second_table.get_column_names())  # new table header consist of parameters headers

    for item in product:
        new_table_row = item[0] + item[1]   # new table row if parameter rows
        for idx, header in enumerate(new_table_headers):
            if header in table_input_dict:
                table_input_dict[header].append(new_table_row[idx])  # creating new table row
            else:
                table_input_dict[header] = [new_table_row[idx]]
    return Table(table_input_dict)

def make_one_table(database, table_names):
    """
    Makes one table, if making cartesian product more than 2 tables
    :param database: database in with we make actions
    :param table_names: list of table names, we want to product
    :return: result of product
    """
    new_table = cartesian_product(database.get_table(table_names[0]), database.get_table(table_names[1]))
    if(len(table_names)>2):
        for i in range(len(table_names)-2):
            new_table = cartesian_product(new_table, database.get_table(table_names[i+2]))
    return new_table

def execute_condition(table, left_param, right_param, sign):
    """
    executes conditions in where block
    :param table: table with input data
    :param left_param: left operand in condition
    :param right_param: right operand in condition
    :param sign: condition sign
    :return: table with applied condition rule
    """
    table_input_dict = {}
    table_headers = table.get_column_names()
    table_rows = table.get_rows()
    left_param_col_index = table_headers.index(left_param)
    if(right_param in table_headers):  # check if right param is table header
        right_param_col_index = table_headers.index(right_param)
        for row in table_rows:  # for each row in table applying the rule
            if(sign=='='):  # using different condition signs
                if (row[left_param_col_index] == row[right_param_col_index]):  # if condition is True, add this row to result table
                    for idx, header in enumerate(table_headers):
                        if header in table_input_dict:
                            table_input_dict[header].append(row[idx])
                        else:
                            table_input_dict[header] = [row[idx]]
            elif(sign=='>'):
                if (row[left_param_col_index] > row[right_param_col_index]):
                    for idx, header in enumerate(table_headers):
                        if header in table_input_dict:
                            table_input_dict[header].append(row[idx])
                        else:
                            table_input_dict[header] = [row[idx]]
    else:  # if right param is constant value
        for row in table_rows:
            if (sign == '='):
                if (row[left_param_col_index] == right_param):
                    for idx, header in enumerate(table_headers):
                        if header in table_input_dict:
                            table_input_dict[header].append(row[idx])
                        else:
                            table_input_dict[header] = [row[idx]]
            elif(sign=='>'):
                if (row[left_param_col_index] > right_param):
                    for idx, header in enumerate(table_headers):
                        if header in table_input_dict:
                            table_input_dict[header].append(row[idx])
                        else:
                            table_input_dict[header] = [row[idx]]
    return Table(table_input_dict)


def remove_unpropper_rows(query_table, conditions):
    """
    function that handles where statements
    :param query_table: input table
    :param conditions: list of conditions that would be applied
    :return:
    """
    if ('=' in conditions[0]):
        params = conditions[0].split('=')
        result_table = execute_condition(query_table, params[0], params[1], '=')
    elif('>' in conditions[0]):
        params = conditions[0].split('>')
        result_table = execute_condition(query_table, params[0], params[1], '>')

    if (len(conditions) > 1):  # if more than one condition, using previous output table
        for condition in conditions:
            if ('=' in conditions[0]):
                params = conditions[0].split('=')
                result_table = execute_condition(result_table, params[0], params[1], '=')
            elif ('>' in conditions[0]):
                params = conditions[0].split('>')
                result_table = execute_condition(result_table, params[0], params[1], '>')

    return result_table


def select_proper_columns(query_table, column_names):
    """
    selects rows specified in query
    :param query_table: table with data
    :param column_names: specified columns in query
    :return: result table
    """
    result_table = {}
    for name in column_names:
        result_table[name] = query_table.get_column_content(name)
    return Table(result_table)


def run_query(database, query):
    """
    main function, handles all query execution
    :param database:
    :param query:
    :return: result of query
    """
    query_params = preprocess_query(query)  # getting query parameters

    if(len(query_params['tables'])>1):  # if more than one table in from statement use cartesian product
        query_table = make_one_table(database, query_params['tables'])
    else:
        query_table = database.get_table(query_params['tables'][0])

    if (len(query_params['constraints'])>0):  # check for constarints
        query_table = remove_unpropper_rows(query_table, query_params['constraints'])

    if(query_params['columns'][0]=='*'):  # check for specified columns
        result_table = select_proper_columns(query_table, query_table.get_column_names())
    else:
        result_table = select_proper_columns(query_table, query_params['columns'])
    return result_table  # return result of query


def preprocess_query(query):
    """
    function for getting query parameters
    :param query: input query
    :return: dictionary with parameters
    """
    query_tokens = re.split(",| ", query)  # splitting query to tokens
    # simple checks for query correctness
    select_token_matches = [(idx, item) for idx, item in enumerate(query_tokens) if item.lower() == "select"]
    if (len(select_token_matches) != 1): raise IOError
    from_token_matches = [(idx, item) for idx, item in enumerate(query_tokens) if item.lower() == "from"]
    if (len(from_token_matches) != 1): raise IOError
    where_token_matches = [(idx, item) for idx, item in enumerate(query_tokens) if item.lower() == "where"]
    if (len(where_token_matches) > 1): raise IOError
    # columns specified in select statement
    selected_columns = get_parameters_from_query_tokens(query_tokens, 1, from_token_matches[0][0])

    if (len(where_token_matches) == 1):  # check for where statement
        selected_tables = get_parameters_from_query_tokens(query_tokens,
                                                           from_token_matches[0][0] + 1,
                                                           where_token_matches[0][0])

        constraints = get_parameters_from_query_tokens(query_tokens, where_token_matches[0][0] + 1, len(query_tokens))

    else:
        selected_tables = get_parameters_from_query_tokens(query_tokens, from_token_matches[0][0] + 1, len(query_tokens))
        # if no constraints, this parameter is empty
        constraints = []
    return {"columns": selected_columns, "tables": selected_tables, "constraints": constraints}

def get_parameters_from_query_tokens(tokens, start_index, end_index):
    """
    removes empty tokens and gets right params
    :param tokens: query tokens
    :param start_index: start slice index
    :param end_index: end slice index
    :return: list of parameters
    """
    return list(filter(len, tokens[start_index:end_index]))

if(__name__ == "__main__"):
    while True:
        query = input("Enter a SQuEaL query, or a blank line to exit:")
        if(query==""): quit()
        try:
            database = read_database()
            result = run_query(database, query)
            print(result)
        except IOError:
            print("Wrong query!")

