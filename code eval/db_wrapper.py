import sqlite3


class DBWrapper:
    con = sqlite3.connect("database.db")

    def __init__(self,init_query):
        self.con.row_factory = sqlite3.Row
        cur = self.con.cursor()
        cur.execute(init_query)

        pass

    def select(self, query, params=()):
        cur = self.con.cursor()
        cur.execute(query, params)
        return cur

    def custom(self, query, params):
        cur = self.con.cursor()
        cur.execute(query, params)
        res = cur.fetchall()
        self.con.commit()
        return res
