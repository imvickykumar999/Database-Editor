
import sqlite3 as sql

def auth_table():
	con = sql.connect('mydb/db_sample.db')
	cur = con.cursor()
	# cur.execute("DROP TABLE IF EXISTS users")

	sql3 ='''
CREATE TABLE IF NOT EXISTS "users" (
"UID"   INTEGER PRIMARY KEY AUTOINCREMENT,
"UNAME" varchar(50) NOT NULL,
"EMAIL" varchar(50) NOT NULL,
"UPASS" varchar(50) NOT NULL
)'''

	cur.execute(sql3)
	con.commit()
	con.close()
	

# auth_table()
