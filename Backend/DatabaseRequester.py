import psycopg2
from configparser import ConfigParser

# TODO : Connection pooling
# TODO : fix error with fetchall() returning none


class DatabaseRequester:
    # get database info from direct arguments
    def __init__(self, host, port, database, user, password):
        self.conn = None
        self.connected = False
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def connect(self):
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    database=self.database,
                    user=self.user,
                    password=self.password
                )
                self.connected = True
                print("DB Connected")
            except psycopg2.DatabaseError as err:
                print("[ERROR] Database Connection Failed\n", err)
                return

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            self.connected = False
            print("DB Closed")

    def query(self, query_string, *argv):
        data = None
        status = None
        if self.conn is None:
            self.connect()
        cur = self.conn.cursor()
        cur.execute(query_string, argv)
        self.conn.commit()
        status = cur.statusmessage
        if cur is not None:
            if "SELECT" in status:
                data = cur.fetchall()
            else:
                data = status
        cur.close()
        self.disconnect()
        return data

# end of class DatabaseRequester
