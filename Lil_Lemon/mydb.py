import mysql.connector

# Connect to MySQL Server
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Oluwatobi09"
)

# Create Database
mycursor = mydb.cursor()
mycursor.execute('CREATE DATABASE Lil_Lemon')
print("Done !")