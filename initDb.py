from DataBase import PostgresDb
from dbConfig import DBConfig

dBConfig = DBConfig()
username = dBConfig.get_conf('username')
password = dBConfig.get_conf('password')
host = dBConfig.get_conf('host')
port = dBConfig.get_conf('port')
db = dBConfig.get_conf('db')

def setup_db():
    postgresDb = PostgresDb(username, password, host, port, db)
    db = postgresDb.connect()
    db.execute("create extension if not exists cube;")
    db.execute("drop table if exists vectors")
    db.execute("create table vectors (id serial, name varchar, vec_low cube, vec_high cube);")
    db.execute("create index vectors_vec_idx on vectors (vec_low, vec_high);")

setup_db()