import psycopg2
from psycopg2 import pool


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
                if "SELECT" in status:
                    data = cur.fetchall()
                else:
                    data = status
            cur.close()
            conn.close()
            print(status)
        except psycopg2.DatabaseError as err:
            print("[ERROR] Database Connection Failed\n", err)

        return data

# end of class DatabaseRequester
