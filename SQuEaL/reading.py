# Functions for reading tables and databases

import csv
import glob
from database import *


# Write the read_table and read_database functions below

def read_table(filename):
    """
    Reads table from .csv file
    :param filename:
    :return: table object
    """
    table_input_dict = {}
    with open(filename, 'r') as csvfile:
        # get cols headers
        header_row = csvfile.readline().rstrip().split(",")
        reader = csv.reader(csvfile)
        # go to next line
        for row in reader:
            for idx,header in enumerate(header_row):
                if header in table_input_dict:
                    table_input_dict[header].append(row[idx].lstrip().rstrip())  # clean row item from spaces
                else:
                    table_input_dict[header] = [row[idx].lstrip().rstrip()]
    return Table(table_input_dict)

def read_database():
    """
    Reads data from all .csv files and creates database
    :return: database object
    """
    file_list = glob.glob('csv_files/*.csv')  # retrieving list of files (check for your file structure)
    database_input_dict = {}
    for file in file_list:
        table = read_table(file)  # for each file create table
        table_name = file[file.rfind("/")+1:file.find(".")]  # taking table name from file
        database_input_dict[table_name] = table  # adding table to database
    return Database(database_input_dict)