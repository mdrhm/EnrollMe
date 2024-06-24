import mysql.connector
from flask import Flask, request, Response
import os
from dotenv import load_dotenv

load_dotenv()
application = Flask(__name__)

mydb = mysql.connector.connect(
  host=os.getenv("DB_HOST"),
  user=os.getenv("DB_USER"),
  password=os.getenv("DB_PASSWORD"),
  port=os.getenv("DB_PORT"),
)

mycursor = mydb.cursor(dictionary=True)
mycursor.execute("USE sql5715671;")

@application.route('/get_courses', methods=['GET'])
def get_courses():
 query = request.args.get('q')
 id = request.args.get('id')
 sql = "SELECT * FROM course"
 if id:
    sql += " WHERE course_id = " + id
 elif query:
    sql += " WHERE CONCAT(course_subject, ' ', course_level, ' ', name) LIKE '%" + query + "%'"
 mycursor.execute(sql + ";")
 arr = []
 for row in mycursor:
    arr += [row]
 return arr


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8000)))
