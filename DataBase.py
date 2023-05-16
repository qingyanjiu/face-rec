import postgresql
import psycopg2

class PostgresDb:

    def __init__ (self, username, password, host, port, db):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.db = db
    
    def connect(self):
        connect_str = 'pq://{}:{}@{}:{}/{}'.format(self.username, self.password, self.host, self.port, self.db)
        db = postgresql.open(connect_str)
        return db
    

class Psycopg2Db:

    def __init__ (self, username, password, host, port, db):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.db = db
    
    def connect(self):
        connect_str = "user='{}' password='{}' host='{}' port='{}' dbname='{}'"\
            .format(self.username, self.password, self.host, self.port, self.db)
        db = psycopg2.connect(connect_str)
        return db