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
        cursor.callproc('RetrieveRoster', [professor_id, section_id])
        studentInfo = []
        for result in cursor.stored_results():
            studentInfo.extend(result.fetchall())
        return studentInfo
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
        cursor.callproc('GetEnrollments', [id])
        sections = []
        for result in cursor.stored_results():
            sections += result.fetchall()
        return list(map(lambda x: {"section_id": x[0],
                                "course_name": x[1],
                                "course_id": x[2],
                                "credits": x[3],
                                "description": x[4],
                                "course_code": x[5],
                                "end_date": x[6],
                                "instruction_mode": x[7],
                                "start_date": x[8],
                                "max_capacity": x[9],
                                "semester": x[10]
                                }, sections))
    except Exception as error:
        return {"error": str(error)}