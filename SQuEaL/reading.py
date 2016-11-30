# Functions for reading tables and databases

import glob
import pandas
from database import *


# Write the read_table and read_database functions below

def read_table(filename):
    table_input_dict = {}
    file_df = pandas.read_csv(filename, dtype=str)
    csv_headers = file_df.columns.values
    for header in csv_headers:
        table_input_dict[header] = list(file_df[header])
    return Table(table_input_dict)


def read_database():
    file_list = glob.glob('csv_files/*.csv')
    database_input_dict = {}
    for file in file_list:
        table = read_table(file)
        table_name = file[file.rfind("/")+1:file.find(".")]
        database_input_dict[table_name] = table
    return Database(database_input_dict)


read_database()