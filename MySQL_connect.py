import mysql.connector
import Password as pw
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=pw.pswd,
    database="Library_Database"
)
cursor = conn.cursor()
