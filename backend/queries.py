import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

mydb = mysql.connector.connect(
  host=os.getenv("DB_HOST"),
  user=os.getenv("DB_USER"),
  password=os.getenv("DB_PASSWORD"),
  port=os.getenv("DB_PORT"),
  autocommit=True
)

mycursor = mydb.cursor(dictionary=True)
mycursor.execute("USE " + os.getenv("DB_NAME") + ";")

def SELECT_FROM_WHERE(s, f, w="1=1"):
    try:
        mycursor.execute("SELECT " + s + " FROM " + f + " WHERE " + w + ";")
        arr = []
        for row in mycursor:
            arr += [row]
        return arr
    except:
        return {"error": "There was an error"}

def INSERT_INTO(t, d):
    try:
        mycursor.execute("INSERT INTO " + t + "(" + ", ".join(list(d.keys())) + ") VALUES ('" + "', '".join(list(d.values())) + "');")
        return {"message": "Insert Successful"}
    except:
        return {"error": "There was an error"}

def DELETE_FROM_WHERE(t, w):
    try:
        mycursor.execute("DELETE FROM " + t + " WHERE " + w + ";")
        return {"message": "Row Deleted"}
    except:
        return {"error": "There was an error"}