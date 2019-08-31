from sqlite3 import connect, OperationalError
from os import remove


class DataCtx:
    """ Data context class for storing scraped data in the database.

    rowcount
      Count of inserted, changed or deleted records.
    """
    __conn = connect('ScrapedData.db')
    __cursor = None

    def __init__(self):
        self.rowcount = 0
        self.__cursor = self.__conn.cursor()

    def execute(self, query: str, *params):
        """ Executes SQl scripts.

        :param query: A query string.
        :param params: A query parameters.
        :return: rowcount.
        """

        return self.__exec(True, query, *params)

    def execute_many(self, query: str, *params):
        """ Executes SQL scripts with many parameters.

        :param query: A query string.
        :param params: A query parameters.
        :return: rowcount.
        """

        return self.__exec(False, query, *params)

    def __exec(self, is_one: bool, query: str, *params):
        if is_one:
            self.__cursor.execute(query, *params)
        else:
            self.__cursor.executemany(query, *params)
        self.rowcount = self.__cursor.rowcount
        self.__conn.commit()

        return self.rowcount

    def select(self, query: str, *params):
        """ Selects rows from a table.

        :param query: A query string.
        :param params: A query parameters.
        :return: A list of selected records.
        """
        self.__cursor.execute(query, *params)
        rows = self.__cursor.fetchall()
        self.rowcount = len(rows)

        return rows

    def save_to_file(self, path: str):
        """ Saves all data from the Teachers table to a file.

        :param path: The path to a file.
        """
        try:
            with open(path, 'w', encoding='utf-8') as out:
                for row in self.select("select * from teachers"):
                    out.write('|'.join([str(i) for i in row]) + '\n')
        except OperationalError:
            remove(path)
            print("There is no table in the database yet! Try again after creating the table.")
        else:
            print("All data has been successfully saved to the file.")

    def __del__(self):
        """ Closes a connection after all operations. """
        self.__conn.close()
