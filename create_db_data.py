import sqlite3 as sql

#connect to SQLite
con = sql.connect('dukcapil.db')

#Create a Connection
cur = con.cursor()


#Drop users table if already exsist.
cur.execute("DROP TABLE IF EXISTS m_dukcapil_data")
cur.execute("DROP TABLE IF EXISTS m_marital_status")
cur.execute("DROP TABLE IF EXISTS m_religion")
# cur.execute("DROP TABLE IF EXISTS t_dukcapil_check_result")

sqlReligion = '''CREATE TABLE "m_religion" (
	"religion_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"religion_name"	TEXT
)'''

sqlMartial = '''CREATE TABLE "m_marital_status" (
	"m_marital_status_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"marital_status_desc"	TEXT
)'''

#Create users table  in db_web database
sqlData ='''CREATE TABLE "m_dukcapil_data" (
	"m_dukcapil_data_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"nik"	TEXT,
	"name"	TEXT,
	"maiden_name"	TEXT,
	"birth_date"	DATE,
	"gender"	CHAR(1),
	"religion_id"	INTEGER,
    "martial_status" INTEGER,
	FOREIGN KEY (religion_id) references m_religion(religion_id),
	FOREIGN KEY (martial_status) references m_marital_status(m_marital_status_id)
)'''

sqlCheck ='''CREATE TABLE "t_dukcapil_check_result" (
	"t_dukcapil_check_result_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"nik_search"	TEXT,
	"time_search"	datetime default CURRENT_TIMESTAMP
)'''


cur.execute(sqlReligion)
cur.execute(sqlMartial)
cur.execute(sqlData)
cur.execute(sqlCheck)

con.commit()

#close the connection
con.close()