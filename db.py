
# connnection mysql


import mysql.connector
conn = mysql.connector.connect(host='localhost',password='admin',user='root')

if conn.is_connected():
    print("connection establish")