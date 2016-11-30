class Table():
    '''A class to represent a SQuEaL table'''

    def __init__(self, new_dict):
        self.table_content = {}
        for key, values in new_dict.items():
            self.table_content[key] = values

    def __repr__(self):
        self.print_csv()
        return ""

    def num_rows(self):
        dict_columns = list(self.table_content.values())
        return len(dict_columns[0])

    def set_dict(self, new_dict):
        '''(Table, dict of {str: list of str}) -> NoneType

        Populate this table with the data in new_dict.
        The input dictionary must be of the form:
            column_name: list_of_values
        '''
        for key, values in new_dict.items():
            self.table_content[key] = values
    def get_dict(self):
        '''(Table) -> dict of {str: list of str}

        Return the dictionary representation of this table. The dictionary keys
        will be the column names, and the list will contain the values
        for that column.
        '''
        output_dict={}
        for key, value in self.table_content.items():
            output_dict[key] = value
        return output_dict

    def print_csv(self):
        '''(Table) -> NoneType
        Print a representation of table in csv format.
        '''
        # no need to edit this one, but you may find it useful (you're welcome)
        dict_rep = self.get_dict()
        columns = list(dict_rep.keys())
        print(','.join(columns))
        rows = self.num_rows()
        for i in range(rows):
            cur_column = []
            for column in columns:
                cur_column.append(dict_rep[column][i])
            print(','.join(cur_column))


class Database():
    '''A class to represent a SQuEaL database'''

    def __init__(self, new_dict):
        self.database_tables = {}
        for key, values in new_dict.items():
            self.database_tables[key] = values

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
