# Functions for reading tables and databases

import glob
import pandas
from database import *


# Write the read_table and read_database functions below

def read_table(filename):
    """
    Reads table from .csv file
    :param filename:
    :return: table object
    """
    table_input_dict = {}
    file_df = pandas.read_csv(filename, dtype=str)  # using pandas to read data from csv
    csv_headers = file_df.columns.values  # getting table headers
    for header in csv_headers:
        table_input_dict[header] = list(file_df[header])  # for each header read column info
    return Table(table_input_dict)


def read_database():
    """
    Reads data from all .csv files and creates database
    :return: database object
    """
    file_list = glob.glob('csv_files/*.csv')  # retrieving list of files
    database_input_dict = {}
    for file in file_list:
        table = read_table(file)  # for each file create table
        table_name = file[file.rfind("/")+1:file.find(".")]  # taking table name from file
        database_input_dict[table_name] = table  # adding table to database
    return Database(database_input_dict)