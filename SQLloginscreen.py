import sqlite3


class dbmanager:
    def __init__(self, dbname):
        self.dbname = dbname

    def execute(self, command):
        con = sqlite3.connect(self.dbname)
        cur = con.cursor()
        result = cur.execute(command).fetchall()
        con.commit()
        con.close()
        return result

    def create_tables(self):
        self.execute("""CREATE TABLE "Users" ("ID"	INTEGER,"Username"	TEXT,"Password"	TEXT,PRIMARY KEY("ID" AUTOINCREMENT));""")
