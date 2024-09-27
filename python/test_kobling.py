import mysql.connector # pip install mysql-connector-python

mydb = mysql.connector.connect(
host="ip_adressen_til_PI",
user="username",
password="password",
database="telefonkatalog")

cursor = mydb.cursor()
cursor.execute("SELECT * FROM person")
resultater = cursor.fetchall()

for dings in resultater:
    print(dings)