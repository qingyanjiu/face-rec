import postgresql


def setup_db():
    db = postgresql.open('pq://postgres:19831226lc@43.143.43.63:5434/face')
    db.execute("create extension if not exists cube;")
    db.execute("drop table if exists vectors")
    db.execute("create table vectors (id serial, file varchar, vec_low cube, vec_high cube);")
    db.execute("create index vectors_vec_idx on vectors (vec_low, vec_high);")


setup_db()