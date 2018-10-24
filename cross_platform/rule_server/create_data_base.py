import MySQLdb

db = MySQLdb.connect("0.0.0.0", "root", "root")
cursor = db.cursor()

cursor.execute("""CREATE DATABASE IF NOT EXISTS rule""")
cursor.execute("""USE rule""")

# Create a Cursor object to execute queries.

import MySQLdb

db = MySQLdb.connect("0.0.0.0", "root", "root")
cursor = db.cursor()

#cursor.execute("""CREATE DATABASE IF NOT EXISTS rule""")
cursor.execute("""USE rule""")

# Create a Cursor object to execute queries.

import MySQLdb

db = MySQLdb.connect("0.0.0.0", "root", "root")
cursor = db.cursor()

cursor.execute("""CREATE DATABASE IF NOT EXISTS rule""")
cursor.execute("""USE rule""")

# Create a Cursor object to execute queries.

import MySQLdb

db = MySQLdb.connect("0.0.0.0", "root", "root")
cursor = db.cursor()

#cursor.execute("""CREATE DATABASE IF NOT EXISTS rule""")
cursor.execute("""USE rule""")

# Create a Cursor object to execute queries.

cursor.execute("""CREATE TABLE IF NOT EXISTS Rule(
        rule_id VARCHAR(100) PRIMARY KEY,
        rule_name TEXT(100) ,
        rule_status VARCHAR(10),
        rule_condition VARCHAR(10000),
        rule_action VARCHAR(10000),
        insert_time INT)  """)


db.commit()
cursor.close()


db.commit()
cursor.close()


db.commit()
cursor.close()


db.commit()
cursor.close()
