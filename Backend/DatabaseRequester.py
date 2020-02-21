import psycopg2
from configparser import ConfigParser

class DatabaseRequester:

    conn = None
    connected = False
    host = None
    port = None
    database = None
    user = None
    password = None

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
            except psycopg2.DatabaseError:
                return

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            self.connected = False
            print("DB Closed")

    def query(self, query_string, *argv):
        data = None
        if self.conn is None:
            self.connect()
        cur = self.conn.cursor()
        cur.execute(query_string, argv)
        self.conn.commit()
        data = cur.fetchall()
        cur.close()
        self.disconnect()
        return data
