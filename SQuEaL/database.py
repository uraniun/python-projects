class Table:
    """A class to represent a SQuEaL table"""

    def __init__(self, new_dict=None):
        """class constructor. without parameters create empty table
        :param new_dict - dictionary to create new table"""
        self.table_content = {}
        if new_dict is not None:
            for key, values in new_dict.items():
                self.table_content[key] = values

    def __repr__(self):
        """
        Function to represent table objects in print statement
        :return:
        """
        self.print_csv()
        return ""

    def get_row_count(self):
        """
        Count rows in table
        :return: int row count in table
        """
        dict_columns = list(self.table_content.values())
        return len(dict_columns[0])

    def get_column_content(self, column_name):
        """
        Get values stored in specified column
        :param column_name:
        :return: list of table column content
        """
        return self.table_content[column_name]

    def get_column_names(self):
        """
        Get names of table columns
        :return: list of table column names
        """
        columns = list(self.table_content.keys())
        return columns

    def get_rows(self):
        """
        Represent table as rows with values
        :return: list of table rows
        """
        table_rows = []  # list for storing all rows
        columns = self.get_column_names()
        for i in range(self.get_row_count()):  # for each row in table
            curr_row = []   # creating row for storing data
            for column in columns:
                curr_row.append(self.table_content[column][i])  # add data to row from each column
            table_rows.append(curr_row)
        return table_rows

    def set_dict(self, new_dict):
        """(Table, dict of {str: list of str}) -> NoneType

        Populate this table with the data in new_dict.
        The input dictionary must be of the form:
            column_name: list_of_values
        """
        for key, values in new_dict.items():
            self.table_content[key] = values

    def get_dict(self):
        """(Table) -> dict of {str: list of str}

        Return the dictionary representation of this table. The dictionary keys
        will be the column names, and the list will contain the values
        for that column.
        """
        output_dict = {}
        for key, value in self.table_content.items():
            output_dict[key] = value
        return output_dict

    def print_csv(self):
        """(Table) -> NoneType
        Print a representation of table in csv format.
        """
        # no need to edit this one, but you may find it useful (you're welcome)
        dict_rep = self.get_dict()
        columns = list(dict_rep.keys())
        print(','.join(columns))
        rows = self.get_row_count()
        for i in range(rows):
            cur_column = []
            for column in columns:
                cur_column.append(dict_rep[column][i])
            print(','.join(cur_column))


class Database:
    '''A class to represent a SQuEaL database'''

    def __init__(self, new_dict=None):
        """class constructor. without parameters create empty database
            :param new_dict - dictionary to create new database"""
        self.database_tables = {}
        if(new_dict is not None):
            for key, values in new_dict.items():
                self.database_tables[key] = values

    def get_table(self, table_name):
        """
        Get specified table
        :param table_name:
        :return: table object
        """
        return self.database_tables[table_name]

    def set_dict(self, new_dict):
        '''(Database, dict of {str: Table}) -> NoneType

        Populate this database with the data in new_dict.
        new_dict must have the format:
            table_name: table
        '''
        for key, value in new_dict.items():
            self.database_tables[key] = value

    def get_dict(self):
        '''(Database) -> dict of {str: Table}

        Return the dictionary representation of this database.
        The database keys will be the name of the table, and the value
        with be the table itself.
        '''
        output_dict = {}
        for key, value in self.database_tables.items():
            output_dict[key] = value
        return output_dict
