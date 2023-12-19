
import sqlite3 as sql

def crud_table():
	con = sql.connect('db_web.db')
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS users")

	sql3 ='''
CREATE TABLE "users" (
"UID"	    INTEGER PRIMARY KEY AUTOINCREMENT,
"UNAME"	    TEXT,
"NAME"	    TEXT,
"FILE"	    TEXT,
"CONTACT"	TEXT
)'''

	cur.execute(sql3)
	con.commit()
	con.close()


def auth_table():
	con = sql.connect('db_sample.db')
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS users")

	sql3 ='''
CREATE TABLE "users" (
"UID"   INTEGER PRIMARY KEY AUTOINCREMENT,
"UNAME" varchar(50) NOT NULL,
"EMAIL" varchar(50) NOT NULL,
"UPASS" varchar(50) NOT NULL
)'''

	cur.execute(sql3)
	con.commit()
	con.close()
	

def db_table(sql3, mydb, table):
	con = sql.connect(mydb)
	cur = con.cursor()
	cur.execute(f"DROP TABLE IF EXISTS {table}")
	
	cur.execute(sql3)
	con.commit()
	con.close()


# mydb = 'db_sample.db'
# table = 'users'

# sql3 = f'''
# CREATE TABLE {table} (
# "UID"	    INTEGER PRIMARY KEY AUTOINCREMENT,
# "UNAME"	    TEXT,
# "NAME"	    TEXT,
# "FILE"	    TEXT,
# "COUNTRY"	TEXT
# )'''

# db_table(sql3, mydb, table)


crud_table()
auth_table()
