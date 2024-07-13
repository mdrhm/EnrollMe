from flask import Flask, request
import hashlib
from queries import SELECT_FROM_WHERE, INSERT_INTO, DELETE_FROM_WHERE, UPDATE_SET_WHERE
application = Flask(__name__)

@application.route('/courses', methods=['GET'])
def courses():
    query = request.args.get('q')
    id = request.args.get('id')
    if id:
        return SELECT_FROM_WHERE("*", "course", "course_id = " + id)
    elif query:
        return SELECT_FROM_WHERE("*", "course", "CONCAT(subject, course_level, name) LIKE '%" + query.replace(" ", "%") + "%'")
    return SELECT_FROM_WHERE("*", "course")

@application.route('/sections', methods=['GET'])
def sections():
    section_id = request.args.get('section')
    course_id = request.args.get('course')
    professor_id = request.args.get('professor')
    where = "1=1"
    if section_id:
        where = "section_id = " + section_id
    elif course_id:
        where =  "section.course_id = " + course_id
    elif professor_id:
        where = "professor_id = " + professor_id
 sections =  SELECT_FROM_WHERE("DISTINCT(section.section_id), course.name AS course_name, section.course_id, course.credits, CONCAT(subject, ' ', course.course_level) AS course_code, section.end_date, section.instruction_mode, section.start_date", "course INNER JOIN section ON course.course_id = section.course_id", where)


    for i in range(len(sections)):
        sections[i]["days"] = SELECT_FROM_WHERE("day, start_time, end_time", "section", "section_id = " + str(sections[i]["section_id"]))
        sections[i]["rooms"] = list(map(lambda x: x["room"], SELECT_FROM_WHERE("DISTINCT(room)", "section", "section_id = " + str(sections[i]["section_id"]))))
        sections[i]["professors"] = SELECT_FROM_WHERE("DISTINCT(professor.professor_id), CONCAT(first_name, ' ', last_name) AS full_name", "professor INNER JOIN section ON section.professor_id = professor.professor_id", "section_id = " + str(sections[i]["section_id"]))
    return sections

@application.route('/professors', methods=['GET', 'POST', 'DELETE', 'PUT'])
def professors():
    if request.method == 'GET':
        query = request.args.get('q')
        id = request.args.get('id')
        if id:
            return SELECT_FROM_WHERE("*, CONCAT(first_name, ' ', last_name) AS full_name", "professor", "professor_id = " + id)
        elif query:
            return SELECT_FROM_WHERE("*, CONCAT(first_name, ' ', last_name) AS full_name", "professor", "CONCAT(first_name, ' ', last_name) LIKE '%" + query.replace(" ", "%") + "%'")
        return SELECT_FROM_WHERE("*, CONCAT(first_name, ' ', last_name) AS full_name", "professor")
    elif request.method == 'POST':
        data = request.json
        professor = {
            "first_name": data.get('first_name'),
            "last_name": data.get('last_name'),
            "email": data.get('email'),
            "phone_number": data.get('phone_number'),
            "department": data.get('department')
        }
        professor_login = {
            "email": data.get('email'),
            "password": None if not data.get('password') else hashlib.sha256(data.get('password').encode('utf-8')).hexdigest()
        }
        if None in professor.values() or None in professor_login.values():
            return {"status": 400, "error": "Invalid data"}, 400
        INSERT_INTO("professor", professor)
        inserted = SELECT_FROM_WHERE("*", "professor", "1=1 ORDER BY professor_id DESC LIMIT 1")[0]
        professor_login["id"] = str(inserted.get("professor_id"))
        INSERT_INTO("login", professor_login)
        return inserted, 201
    elif request.method == 'DELETE':
      data = request.json
      professor_id = str(data.get('id'))
      if not professor_id:
        return {"status": 400, "error": "Invalid Professor ID"}, 400
      DELETE_FROM_WHERE("login", "id=" + professor_id)
      return DELETE_FROM_WHERE("professor", "professor_id=" + professor_id)
    elif request.method == 'PUT':
        data = request.json
        professor_id = str(data.get("id"))
        if not professor_id:
            return {"status": 400, "error": "Invalid Professor ID"}, 400
        del data['id']
        if data.get('password'):
            password_updated = UPDATE_SET_WHERE("login", {"password" : hashlib.sha256(data.get('password').encode('utf-8')).hexdigest()}, "id = " + professor_id)
            del data['password']
            del password_updated['password']
            if len(data) == 0:
                return password_updated
        if data.get('email'):
            UPDATE_SET_WHERE("login", {"email" : data.get('email')}, "id = " + professor_id)
        return UPDATE_SET_WHERE("professor", data, "professor_id = " + professor_id)[0]

@application.route('/students', methods=['GET', 'POST', 'DELETE', 'PUT'])
def students():
    if request.method == 'POST':
        data = request.json
        student = {
            "first_name": data.get('first_name'),
            "last_name": data.get('last_name'),
            "email": data.get('email'),
            "phone_number": data.get('phone_number'),
            "dob": data.get('dob'),
            "sex": data.get('sex'),
            "major": data.get('major')
        }
        student_login = {
            "email": data.get('email'),
            "password": None if not data.get('password') else hashlib.sha256(data.get('password').encode('utf-8')).hexdigest()
        }
        if None in student.values() or None in student_login.values():
            return {"status": 400, "error": "Invalid data"}, 400
        INSERT_INTO("student", student)
        inserted = SELECT_FROM_WHERE("*", "student", "1=1 ORDER BY student_id DESC LIMIT 1")[0]
        student_login["id"] = str(inserted.get("student_id"))
        INSERT_INTO("login", student_login)
        return inserted, 201
    elif request.method == 'DELETE':
      data = request.json
      student_id = str(data.get('id'))
      if not student_id:
        return {"status": 400, "error": "Invalid Student ID"}, 400
      DELETE_FROM_WHERE("login", "id=" + student_id)
      return DELETE_FROM_WHERE("student", "student_id=" + student_id)
    elif request.method == 'PUT':
        data = request.json
        student_id = str(data.get("id"))
        if not student_id:
            return {"status": 400, "error": "Invalid Student ID"}, 400
        del data['id']
        if data.get('password'):
            password_updated = UPDATE_SET_WHERE("login", {"password" : hashlib.sha256(data.get('password').encode('utf-8')).hexdigest()}, "id = " + student_id)[0]
            del data['password']
            del password_updated['password']
            if len(data) == 0:
                return password_updated
        if data.get('email'):
            UPDATE_SET_WHERE("login", {"email" : data.get('email')}, "id = " + student_id)
        return UPDATE_SET_WHERE("student", data, "student_id = " + student_id)[0]

@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        data = request.json
        id = str(data.get('id'))
        password = hashlib.sha256(data.get('password').encode('utf-8')).hexdigest()
        email = data.get('email')
        account_type = data.get('account_type')
        where = ''
        if id and password:
            where = "login.id='" + id + "' AND password='" + password + "'"
        elif email and password:
            where = "login.email='" + email + "' AND password='" + password + "'"
        else:
            return {"status": 400, "error": "One of ID, email, or password wasn't provided"}, 400
        student = SELECT_FROM_WHERE("student_id, first_name, last_name, student.email, phone_number, dob, sex, major, CONCAT(first_name, ' ', last_name) AS full_name", "student INNER JOIN login ON login.id=student.student_id", where)
        professor = SELECT_FROM_WHERE("professor_id, first_name, last_name, professor.email, phone_number, department, CONCAT(first_name, ' ', last_name) AS full_name", "professor INNER JOIN login ON login.id=professor.professor_id", where)
        if account_type == 'student' and len(student) > 0:
            return student[0]
        elif account_type == 'professor' and len(professor) > 0:
            return professor[0]
        return {"status": 401, "error": "Invalid login credentials"}, 401
if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True, port=8000)

