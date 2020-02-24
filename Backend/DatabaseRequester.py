import psycopg2
from psycopg2 import pool

import DataStructures


class DatabaseRequester:
    # get database info from direct arguments
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

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
                # create return object data if query is SELECT
                if "SELECT" in status:
                    colnames = [desc[0] for desc in cur.description] # name of each column
                    rows = cur.fetchall()  # all the rows returned
                    data = QueryTuples(colnames, rows)

            cur.close()
            conn.close()
            print(status)
        except psycopg2.DatabaseError as err:
            print("[ERROR] Database Connection Failed\n", err)

        return data

# end of class DatabaseRequester


# data class containing column names and all the rows returned by query
class QueryTuples:

    def __init__(self, colnames, rows):
        self.colnames = colnames
        self.rows = rows

    def rows_count(self):
        return len(self.rows)

    def columns_count(self):
        return len(self.colnames)

    def get_rows(self):
        return self.rows

    def get_column_names(self):
        return self.colnames
