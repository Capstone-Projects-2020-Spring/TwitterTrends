import psycopg2
from psycopg2 import pool
import traceback

import DataStructures


class DatabaseRequester:
    # get database info from direct arguments
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    # query to the database using the query string then Return a QueryTuples object
    # The QueryTuples object will always contain a status message:
    #       Status message string can be SELECT, INSERT, UPDATE, or DELETE,
    #       along with the numbers of rows affected
    # colnames and rows attributes are empty arrays if query is anything else other than SELECT
    def query(self, query_string, *argv):
        data = None
        try:
            status = None
            conn = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    user=self.user,
                    password=self.password)
            cur = conn.cursor()
            cur.execute(query_string, argv)
            conn.commit()

            status = cur.statusmessage

            if cur is not None:

                if "SELECT" in status:
                    colnames = [desc[0] for desc in cur.description] # name of each column
                    rows = cur.fetchall()  # all the rows returned
                    data = QueryTuples(colnames, rows, status)
                else:
                    data = QueryTuples([], [], status)

            cur.close()
            conn.close()
            print(status)
        except psycopg2.DatabaseError as err:
            print("[ERROR] Database Connection Failed\n", err)
            traceback.print_exc()

        return data

# end of class DatabaseRequester


# data class containing column names and all the rows returned by query
# contain a string representing the type and status of the query
class QueryTuples:

    def __init__(self, colnames, rows, status):
        self.status = status
        self.colnames = colnames
        self.rows = rows

    def get_status_message(self):
        return self.status

    def rows_count(self):
        return len(self.rows)

    def columns_count(self):
        return len(self.colnames)

    def get_rows(self):
        return self.rows

    def get_column_names(self):
        return self.colnames
