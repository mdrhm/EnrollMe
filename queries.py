import csv
from io import StringIO
import os
import pandas as pd
import sqlalchemy as db
import sqlite3

engine = db.create_engine('sqlite:///enrollme.db')

conn = sqlite3.connect('enrollme.db', check_same_thread=False)
cursor = conn.cursor()

def SELECT_FROM_WHERE(s, f, w="1=1"):
    try:
        with engine.connect() as connection:
            return pd.DataFrame(connection.execute(db.text("SELECT " + s + " FROM " + f + " WHERE " + w + ";")).fetchall()).to_dict('records')
    except Exception as error:
        return {"error": str(error)}

def INSERT_INTO(t, d):
    try:
        cursor.execute("INSERT INTO " + t + "(" + ", ".join(list(d.keys())) + ") VALUES ('" + "', '".join(list(map(lambda value: str(value), d.values()))) + "');")
        conn.commit()
        return {"message": "Insert Successful", "inserted": d}
    except Exception as error:
        return {"error": str(error)}

def DELETE_FROM_WHERE(t, w):
    try:
        cursor.execute("DELETE FROM " + t + " WHERE " + w + ";")
        conn.commit()
        return {"message": "Deletion Successful"}
    except Exception as error:
        return {"error": str(error)}

def UPDATE_SET_WHERE(t, s, w):
    try:
        set = list(map(lambda key: str(key + " = '" + str(s[key]) + "'"), s.keys()))
        cursor.execute("UPDATE " + t + " SET " + ", ".join(set) + " WHERE " + w + ";")
        conn.commit()
        return SELECT_FROM_WHERE("*", t, w)
    except Exception as error:
        return {"error": str(error)}

def retrieve_roster(professor_id, section_id):
    try:
        roster = SELECT_FROM_WHERE("student.student_id, first_name, last_name, email, major", "student INNER JOIN enrollment ON student.student_id=enrollment.student_id", "section_id=" + str(section_id) + " GROUP BY last_name, first_name")
        list(map(lambda x : [x["student_id"], x["first_name"], x["last_name"], x["email"], x["major"]], roster))
        return list(map(lambda x : x.values(), roster))
    except Exception as error:
        print(str(error))
        return {"error": str(error)}


def generate_csv(data):
    string_buffer = StringIO()
    csv_writer = csv.writer(string_buffer)
    csv_writer.writerows(data)
    string_buffer.seek(0)
    return string_buffer.getvalue()

def get_enrollment(id):
    try:
        return SELECT_FROM_WHERE("DISTINCT (section.section_id), course.name AS course_name, section.course_id, course.credits, course.description, CONCAT(subject, ' ', course.course_level) AS course_code, semester.end_date, section.instruction_mode, semester.start_date, section.max_capacity, CONCAT(semester.season, ' ', LEFT(semester.start_date, 4)) AS semester", "course INNER JOIN section ON course.course_id = section.course_id INNER JOIN enrollment ON enrollment.section_id = section.section_id INNER JOIN semester ON section.semester_id = semester.semester_id", "enrollment.student_id = id;")
    except Exception as error:
        return {"error": str(error)}