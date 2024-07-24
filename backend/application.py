from flask import Flask, Response, request
import hashlib
from queries import SELECT_FROM_WHERE, INSERT_INTO, DELETE_FROM_WHERE, UPDATE_SET_WHERE, generate_csv, retrieve_roster
application = Flask(__name__)

@application.route('/courses', methods=['GET', 'POST', 'DELETE', 'PUT'])
def courses():
    match request.method:
        case 'GET':
            query = request.args.get('q')
            id = request.args.get('id')
            if id:
                return SELECT_FROM_WHERE("*", "course", "course_id = " + id)
            elif query:
                return SELECT_FROM_WHERE("*", "course", "CONCAT(subject, course_level, name) LIKE '%" + query.replace(" ", "%") + "%'")
            return SELECT_FROM_WHERE("*", "course")
        case 'POST':
            body = request.json
            last_course_id = SELECT_FROM_WHERE("MAX(course_id)", "course")[0]["MAX(course_id)"]
            body["course_id"] = 1 if str(last_course_id) == 'None' else last_course_id + 1
            return INSERT_INTO("course", body)
        case 'DELETE':
            body = request.json
            course_id = body.get('course_id')
            if not course_id:
                return {"status": 400, "error": "Invalid Course ID"}, 400
            return DELETE_FROM_WHERE('course', 'course_id=' + str(course_id))
        case 'PUT':
            body = request.json
            course_id = str(body.get('course_id'))
            del body['course_id']
            return UPDATE_SET_WHERE("course", body, "course_id = " + course_id)[0]

@application.route('/sections', methods=['GET', 'POST', 'DELETE', 'PUT'])
def sections():
    match request.method:
        case 'GET':
            section_id = request.args.get('section')
            course_id = request.args.get('course')
            professor_id = request.args.get('professor')
            where = "1=1"
            if section_id:
                where = "section_id = " + section_id
            elif course_id:
                where =  "section.course_id = " + course_id
            elif professor_id:
                where = "meeting.professor_id = " + professor_id
            sections =  SELECT_FROM_WHERE("DISTINCT(section.section_id), course.name AS course_name, section.course_id, course.credits, course.description, CONCAT(subject, ' ', course.course_level) AS course_code, semester.end_date, section.instruction_mode, semester.start_date, section.max_capacity, CONCAT(semester.season, ' ', LEFT(semester.start_date, 4)) AS semester", "course INNER JOIN section ON course.course_id = section.course_id INNER JOIN semester ON section.semester_id=semester.semester_id INNER JOIN meeting ON section.section_id=meeting.section_id", where)
            for i in range(len(sections)):
                sections[i]["meeting_times"] = SELECT_FROM_WHERE("day, CONCAT(start_time, '') AS start_time, CONCAT(end_time, '') AS end_time", "meeting", "section_id = " + str(sections[i]["section_id"]))
                sections[i]["rooms"] = list(map(lambda x: x["room"], SELECT_FROM_WHERE("DISTINCT(room)", "meeting", "section_id = " + str(sections[i]["section_id"]))))
                sections[i]["professors"] = SELECT_FROM_WHERE("DISTINCT(professor.professor_id), CONCAT(first_name, ' ', last_name) AS full_name", "professor INNER JOIN meeting ON meeting.professor_id = professor.professor_id", "section_id = " + str(sections[i]["section_id"]))
                sections[i]["roster"] = SELECT_FROM_WHERE("DISTINCT(student.student_id), first_name, last_name, email, major", "student INNER JOIN enrollment on student.student_id=enrollment.student_id INNER JOIN section ON enrollment.section_id=section.section_id", "section.section_id=" + str(sections[i]["section_id"]))
                sections[i]["enrolled"] = len(sections[i]["roster"])
            return sections
        case 'POST':
            body = request.json
            last_section_id = SELECT_FROM_WHERE("MAX(section_id)", "section")[0].get("MAX(section_id)")
            body["section_id"] = 1000 if str(last_section_id) == 'None' else last_section_id + 1
            section = {
                "section_id": body.get('section_id'),
                "course_id": body.get('course_id'),
                "max_capacity": body.get('max_capacity'),
                "semester_id": body.get('semester_id'),
                "instruction_mode": body.get('instruction_mode'),
            }
            for key in section.keys():
                if not section.get(key):
                    del section[key]
            INSERT_INTO("section", section)
            section_id = SELECT_FROM_WHERE("MAX(section_id)", "section")[0]["MAX(section_id)"]
            for day in body.get("meeting_times"):
                meeting = {
                    "section_id": body.get('section_id'),
                    "day": day.get("day"),
                    "start_time": day.get("start_time"),
                    "end_time": day.get("end_time"),
                    "professor_id": day.get('professor_id'),
                    "room": day.get('room')
                }
                for key in meeting.keys():
                    if not meeting.get(key):
                        del meeting[key]
                INSERT_INTO('meeting', meeting)
            return {"message": "Insert Successful", "inserted": body}
        case 'DELETE':
            body = request.json
            section_id = body.get('section_id')
            if not section_id:
                return {"status": 400, "error": "Invalid Section ID"}, 400
            DELETE_FROM_WHERE('meeting', 'section_id=' + str(section_id))
            return DELETE_FROM_WHERE('section', 'section_id=' + str(section_id))
        case 'PUT':
            body = request.json
            section_id = body.get('section_id')
            if not section_id:
                return {"status": 400, "error": "Invalid Section"}, 400
            if body.get('meeting_times'):
                DELETE_FROM_WHERE("meeting", "section_id=" + str(section_id))
                for day in body.get('meeting_times'):
                    meeting = {
                        "section_id": section_id,
                        "day": day.get("day"),
                        "start_time": day.get("start_time"),
                        "end_time": day.get("end_time"),
                        "professor_id": day.get('professor_id'),
                        "room": day.get('room')
                    }
                    for key in meeting.keys():
                        if not meeting[key]:
                            del meeting[key]
                    INSERT_INTO('meeting', meeting)
                del body['meeting_times']
            UPDATE_SET_WHERE("section", body, "section_id = " + str(section_id))
            return {"message": "Update Successful", "updated": body}
@application.route('/professors', methods=['GET', 'POST', 'DELETE', 'PUT'])
def professors():
    match request.method:
        case 'GET':
            query = request.args.get('q')
            id = request.args.get('id')
            if id:
                return SELECT_FROM_WHERE("*, CONCAT(first_name, ' ', last_name) AS full_name", "professor", "professor_id = " + id)
            elif query:
                return SELECT_FROM_WHERE("*, CONCAT(first_name, ' ', last_name) AS full_name", "professor", "CONCAT(first_name, ' ', last_name) LIKE '%" + query.replace(" ", "%") + "%'")
            return SELECT_FROM_WHERE("*, CONCAT(first_name, ' ', last_name) AS full_name", "professor")
        case 'POST':
            body = request.json
            professor = {
                "first_name": body.get('first_name'),
                "last_name": body.get('last_name'),
                "email": body.get('email'),
                "phone_number": body.get('phone_number'),
                "department": body.get('department')
            }
            professor_login = {
                "email": body.get('email'),
                "password": None if not body.get('password') else hashlib.sha256(body.get('password').encode('utf-8')).hexdigest()
            }
            if None in professor.values() or None in professor_login.values():
                return {"status": 400, "error": "Invalid body"}, 400
            INSERT_INTO("professor", professor)
            inserted = SELECT_FROM_WHERE("*", "professor", "1=1 ORDER BY professor_id DESC LIMIT 1")[0]
            professor_login["professor_id"] = str(inserted.get("professor_id"))
            INSERT_INTO("login", professor_login)
            return inserted, 201
        case 'DELETE':
          body = request.json
          professor_id = str(body.get('professor_id'))
          if not professor_id:
            return {"status": 400, "error": "Invalid Professor ID"}, 400
          DELETE_FROM_WHERE("login", "id=" + professor_id)
          return DELETE_FROM_WHERE("professor", "professor_id=" + professor_id)
        case 'PUT':
            body = request.json
            professor_id = str(body.get("professor_id"))
            if not professor_id:
                return {"status": 400, "error": "Invalid Professor ID"}, 400
            del body['id']
            if body.get('new_password'):
                if len(SELECT_FROM_WHERE("id", "login", "id = " + professor_id + " AND password ='" + hashlib.sha256(body.get('old_password').encode('utf-8')).hexdigest() + "'")) == 0:
                    return {"status": 404, "error": "Current password doesn't match our records"}, 404
                password_updated = UPDATE_SET_WHERE("login", {"password" : hashlib.sha256(body.get('new_password').encode('utf-8')).hexdigest()}, "id = " + professor_id)[0]
                del body['old_password']
                del body['new_password']
                del password_updated['password']
                if len(body) == 0:
                    return password_updated
            if body.get('email'):
                UPDATE_SET_WHERE("login", {"email" : body.get('email')}, "id = " + professor_id)
            return UPDATE_SET_WHERE("professor", body, "professor_id = " + professor_id)[0]

@application.route('/students', methods=['GET', 'POST', 'DELETE', 'PUT'])
def students():
    match request.method:
        case 'POST':
            body = request.json
            student = {
                "first_name": body.get('first_name'),
                "last_name": body.get('last_name'),
                "email": body.get('email'),
                "phone_number": body.get('phone_number'),
                "dob": body.get('dob'),
                "sex": body.get('sex'),
                "major": body.get('major')
            }
            student_login = {
                "email": body.get('email'),
                "password": None if not body.get('password') else hashlib.sha256(body.get('password').encode('utf-8')).hexdigest()
            }
            if None in student.values() or None in student_login.values():
                return {"status": 400, "error": "Invalid body"}, 400
            INSERT_INTO("student", student)
            inserted = SELECT_FROM_WHERE("*", "student", "1=1 ORDER BY student_id DESC LIMIT 1")[0]
            student_login["student_id"] = str(inserted.get("student_id"))
            INSERT_INTO("login", student_login)
            return inserted, 201
        case 'DELETE':
          body = request.json
          student_id = str(body.get('student_id'))
          if not student_id:
            return {"status": 400, "error": "Invalid Student ID"}, 400
          DELETE_FROM_WHERE("login", "id=" + student_id)
          return DELETE_FROM_WHERE("student", "student_id=" + student_id)
        case 'PUT':
            body = request.json
            student_id = str(body.get("student_id"))
            if not student_id:
                return {"status": 400, "error": "Invalid Student ID"}, 400
            del body['id']
            if body.get('new_password'):
                if len(SELECT_FROM_WHERE("id", "login", "id = " + student_id + " AND password ='" + hashlib.sha256(body.get('old_password').encode('utf-8')).hexdigest() + "'")) == 0:
                    return {"status": 404, "error": "Current password doesn't match our records"}, 404
                password_updated = UPDATE_SET_WHERE("login", {"password" : hashlib.sha256(body.get('new_password').encode('utf-8')).hexdigest()}, "id = " + student_id)[0]
                del body['old_password']
                del body['new_password']
                del password_updated['password']
                if len(body) == 0:
                    return password_updated
            if body.get('email'):
                UPDATE_SET_WHERE("login", {"email" : body.get('email')}, "id = " + student_id)
            return UPDATE_SET_WHERE("student", body, "student_id = " + student_id)[0]

@application.route('/login', methods=['GET', 'POST'])
def login():
    match request.method:
        case 'POST':
            body = request.json
            username = str(body.get('username'))
            password = hashlib.sha256(body.get('password').encode('utf-8')).hexdigest()
            account_type = body.get('account_type')
            if not username or not password:
                return {"status": 400, "error": "Email/ID or password wasn't provided"}, 400
            user = None
            if account_type == 'student':
                user = SELECT_FROM_WHERE("student.student_id, first_name, last_name, student.email, phone_number, dob, sex, major, CONCAT(first_name, ' ', last_name) AS full_name", "student INNER JOIN login ON login.student_id=student.student_id", "(login.student_id = '" + username + "' OR login.email = '" + username + "') AND password='" + password + "'")
            elif account_type == 'professor':
                user = SELECT_FROM_WHERE("professor.professor_id, first_name, last_name, professor.email, phone_number, department, CONCAT(first_name, ' ', last_name) AS full_name", "professor INNER JOIN login ON login.professor_id=professor.professor_id", "(login.professor_id = '" + username + "' OR login.email = '" + username + "') AND password='" + password + "'")
            if not user or len(user) == 0:
                return {"status": 401, "error": "Invalid login credentials"}, 401
            return user[0]

@application.route('/enrollments', methods=['GET', 'POST', 'DELETE', 'PUT'])
def enrollments():
    match request.method:
        case 'GET':
            id = request.args.get('id')
            if not id:
                return {"status": 401, "error": "Invalid Student ID"}, 401
            schedule =  SELECT_FROM_WHERE("DISTINCT(section.section_id), course.name AS course_name, section.course_id, course.credits, course.description, CONCAT(subject, ' ', course.course_level) AS course_code, semester.end_date, section.instruction_mode, semester.start_date, section.max_capacity, CONCAT(semester.season, ' ', LEFT(semester.start_date, 4)) AS semester", "course INNER JOIN section ON course.course_id = section.course_id INNER JOIN enrollment ON enrollment.section_id=section.section_id INNER JOIN semester ON section.semester_id=semester.semester_id", "enrollment.student_id=" + id)
            for i in range(len(schedule)):
                schedule[i]["meeting_times"] = SELECT_FROM_WHERE("day, CONCAT(start_time, '') AS start_time, CONCAT(end_time, '') AS end_time", "meeting", "section_id = " + str(schedule[i]["section_id"]))
                schedule[i]["rooms"] = list(map(lambda x: x["room"], SELECT_FROM_WHERE("DISTINCT(room)", "meeting", "section_id = " + str(schedule[i]["section_id"]))))
                schedule[i]["professors"] = SELECT_FROM_WHERE("DISTINCT(professor.professor_id), CONCAT(first_name, ' ', last_name) AS full_name", "professor INNER JOIN meeting ON meeting.professor_id = professor.professor_id", "section_id = " + str(schedule[i]["section_id"]))
                schedule[i]["enrolled"] = SELECT_FROM_WHERE("COUNT(*)", "enrollment", "section_id = " + str(schedule[i]["section_id"]))[0]["COUNT(*)"]
            return schedule
        case 'POST':
            body = request.json
            enrollment = {
                "student_id": str(body.get("student_id")),
                "section_id": str(body.get("section_id"))
            }
            if str(None) in enrollment.values():
                return {"status": 400, "error": "Invalid body"}, 400
            return INSERT_INTO("enrollment", enrollment)
        case 'DELETE':
            body = request.json
            student_id = str(body.get("student_id"))
            section_id = str(body.get("section_id"))
            return DELETE_FROM_WHERE("enrollment", "student_id=" + student_id + " AND section_id=" + section_id)
        case 'PUT':
            body = request.json
            student_id = str(body.get('student_id'))
            sections = list(map(lambda x: str(x), body.get('sections')))
            sections_str = "('')" if not sections else "(" + ", ".join(sections) + ")"
            DELETE_FROM_WHERE("enrollment", "student_id = " + student_id + " AND NOT section_id in " + sections_str)
            already_enrolled = list(map(lambda x: str(x["section_id"]), SELECT_FROM_WHERE("section_id","enrollment", "student_id = " + student_id + " AND section_id in " + sections_str)))
            sections_to_add = filter(lambda x: x not in already_enrolled, sections)
            for section in sections_to_add:
                INSERT_INTO("enrollment", {"student_id": student_id,
                "section_id": section})
            return {"message": "Schedule Updated Successful", "updated": body}


@application.route('/roster', methods=['GET'])
def download_roster():
    id = request.args.get('id')
    if not id:
        return {"status": 400, "error": "Invalid Professor ID"}, 400

    data = retrieve_roster(id)
    if not data:
        return {"status": 400, "error": "Empty Roster"}, 400

    csv_data = generate_csv(data)
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=roster.csv"}
    )

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True, port=8000)