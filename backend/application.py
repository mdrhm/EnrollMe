from flask import Flask, request, render_template, session, redirect, Response
import os
import hashlib
from datetime import date
from queries import SELECT_FROM_WHERE, INSERT_INTO, DELETE_FROM_WHERE, UPDATE_SET_WHERE, enroll_student, generate_csv, retrieve_roster
from ai import generate_course


application = Flask(__name__)
application.config["SESSION_PERMANENT"] = False
application.secret_key = os.urandom(24)

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
            sections =  SELECT_FROM_WHERE("DISTINCT(section.section_id), course.name AS course_name, section.course_id, course.credits, course.description, CONCAT(subject, ' ', course.course_level) AS course_code, semester.end_date, section.instruction_mode, semester.start_date, section.max_capacity, CONCAT(semester.season, ' ', LEFT(semester.start_date, 4)) AS semester", "course INNER JOIN section ON course.course_id = section.course_id INNER JOIN semester ON section.semester_id=semester.semester_id LEFT JOIN meeting ON section.section_id=meeting.section_id", where)
            for i in range(len(sections)):
                sections[i]["meeting_times"] = SELECT_FROM_WHERE("day, CONCAT(start_time, '') AS start_time, CONCAT(end_time, '') AS end_time, room, CONCAT(first_name, ' ', last_name) AS professor", "meeting INNER JOIN professor ON meeting.professor_id=professor.professor_id", "section_id = " + str(sections[i]["section_id"]))
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
            session['id'] = inserted.get("professor_id")
            session['account_type'] = 'professor'
            return inserted, 201
        case 'DELETE':
          body = request.json
          professor_id = str(body.get('professor_id'))
          if not professor_id:
            return {"status": 400, "error": "Invalid Professor ID"}, 400
          DELETE_FROM_WHERE("login", "professor_id=" + professor_id)
          return DELETE_FROM_WHERE("professor", "professor_id=" + professor_id)
        case 'PUT':
            body = request.json
            professor_id = str(body.get("professor_id"))
            if not professor_id:
                return {"status": 400, "error": "Invalid Professor ID"}, 400
            del body['professor_id']
            if body.get('new_password'):
                if len(SELECT_FROM_WHERE("professor_id", "login", "professor_id = " + professor_id + " AND password ='" + hashlib.sha256(body.get('old_password').encode('utf-8')).hexdigest() + "'")) == 0:
                    return {"status": 404, "error": "Current password doesn't match our records"}, 404
                password_updated = UPDATE_SET_WHERE("login", {"password" : hashlib.sha256(body.get('new_password').encode('utf-8')).hexdigest()}, "professor_id = " + professor_id)[0]
                del body['old_password']
                del body['new_password']
                del password_updated['password']
                if len(body) == 0:
                    return password_updated
            if body.get('email'):
                UPDATE_SET_WHERE("login", {"email" : body.get('email')}, "professor_id = " + professor_id)
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
            session['id'] = inserted.get("student_id")
            session['account_type'] = 'student'
            return inserted, 201
        case 'DELETE':
          body = request.json
          student_id = str(body.get('student_id'))
          if not student_id:
            return {"status": 400, "error": "Invalid Student ID"}, 400
          DELETE_FROM_WHERE("login", "student_id=" + student_id)
          return DELETE_FROM_WHERE("student", "student_id=" + student_id)
        case 'PUT':
            body = request.json
            student_id = str(body.get("student_id"))
            if not student_id:
                return {"status": 400, "error": "Invalid Student ID"}, 400
            del body['student_id']
            if body.get('new_password'):
                if len(SELECT_FROM_WHERE("student_id", "login", "student_id = " + student_id + " AND password ='" + hashlib.sha256(body.get('old_password').encode('utf-8')).hexdigest() + "'")) == 0:
                    return {"status": 404, "error": "Current password doesn't match our records"}, 404
                password_updated = UPDATE_SET_WHERE("login", {"password" : hashlib.sha256(body.get('new_password').encode('utf-8')).hexdigest()}, "student_id = " + student_id)[0]
                del body['old_password']
                del body['new_password']
                del password_updated['password']
                if len(body) == 0:
                    return password_updated
            if body.get('email'):
                UPDATE_SET_WHERE("login", {"email" : body.get('email')}, "student_id = " + student_id)
            return UPDATE_SET_WHERE("student", body, "student_id = " + student_id)[0]

@application.route('/login', methods=['GET', 'POST'])
def login():
    match request.method:
        case 'GET':
            return redirect('/')
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
            session['id'] = user[0][account_type + "_id"]
            session['account_type'] = account_type
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
                schedule[i]["meeting_times"] = SELECT_FROM_WHERE("day, CONCAT(start_time, '') AS start_time, CONCAT(end_time, '') AS end_time, room, CONCAT(professor.first_name, ' ', professor.last_name) AS professor", "meeting INNER JOIN professor ON meeting.professor_id=professor.professor_id", "section_id = " + str(schedule[i]["section_id"]))
                schedule[i]["rooms"] = list(map(lambda x: x["room"], SELECT_FROM_WHERE("DISTINCT(room)", "meeting", "section_id = " + str(schedule[i]["section_id"]))))
                schedule[i]["professors"] = SELECT_FROM_WHERE("DISTINCT(professor.professor_id), CONCAT(first_name, ' ', last_name) AS full_name", "professor INNER JOIN meeting ON meeting.professor_id = professor.professor_id", "section_id = " + str(schedule[i]["section_id"]))
                schedule[i]["enrolled"] = SELECT_FROM_WHERE("COUNT(*)", "enrollment", "section_id = " + str(schedule[i]["section_id"]))[0]["COUNT(*)"]
            return schedule
        case 'POST':
            body = request.json
            enrollment = {
                "student_id": str(body.get("student_id")),
                "section_id": str(body.get("section_id")),
                "status": ''
            }
            if str(None) in enrollment.values():
                return {"status": 400, "error": "Invalid body"}, 400
            return enroll_student(enrollment["student_id"], enrollment["section_id"], enrollment["status"])
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
                enroll_student(student_id, section, '')
            return {"message": "Schedule Updated Successful", "updated": body}


@application.route('/roster', methods=['GET'])
def download_roster():
    professor_id = request.args.get("professor")
    if not professor_id:
        return {"status": 400, "error": "Invalid Professor ID"}, 400
    section_id = request.args.get("section")
    if not section_id:
        return {"status": 400, "error": "Invalid Section ID"}, 400
    if not professor_id == str(session.get('id')):
        return {"status": 400, "error": "Professor ID not authenticated"}, 400
    data = [['Student ID', 'First Name', 'Last Name', 'Email', 'Major']] + retrieve_roster(professor_id, section_id)
    course_code = SELECT_FROM_WHERE("CONCAT(subject, '_', course_level) as course_code", "course INNER JOIN section ON section.course_id=course.course_id", "section.section_id=" + section_id)[0]["course_code"]
    csv_data = generate_csv(data)
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=" + course_code + "_" + section_id + "_Roster.csv"}
    )

@application.route('/')
def index():
    return render_template('login.html')

@application.route('/register')
def signup():
    return render_template('signup.html')

@application.route('/dashboard')
def professor_dashboard():
    if not session.get('id') or not session.get('account_type'):
        return redirect('/')
    if session.get('account_type') == 'student':
        return redirect('/enroll')
    return render_template('dashboard.html', page_title = "MyDashboard", id=session['id'], user = SELECT_FROM_WHERE("*", session.get('account_type'), session.get('account_type') + "_id = " + str(session['id']))[0], account_type = session.get('account_type'))

@application.route('/enroll')
def student_enroll():
    if not session.get('id') or not session.get('account_type'):
        return redirect('/')
    if session.get('account_type') == 'professor':
        return redirect('/dashboard')
    sections =  SELECT_FROM_WHERE("DISTINCT(section.section_id), course.name AS course_name, section.course_id, course.credits, course.description, CONCAT(subject, ' ', course.course_level) AS course_code, CONCAT(semester.end_date, '') AS end_date, section.instruction_mode, CONCAT(semester.start_date, '') AS start_date, section.max_capacity, CONCAT(semester.season, ' ', LEFT(semester.start_date, 4)) AS semester", "course INNER JOIN section ON course.course_id = section.course_id INNER JOIN semester ON section.semester_id=semester.semester_id")
    for i in range(len(sections)):
        sections[i]["meeting_times"] = SELECT_FROM_WHERE("day, CONCAT(start_time, '') AS start_time, CONCAT(end_time, '') AS end_time", "meeting", "section_id = " + str(sections[i]["section_id"]))
        sections[i]["rooms"] = list(map(lambda x: x["room"], SELECT_FROM_WHERE("DISTINCT(room)", "meeting", "section_id = " + str(sections[i]["section_id"]))))
        sections[i]["professors"] = SELECT_FROM_WHERE("DISTINCT(professor.professor_id), CONCAT(first_name, ' ', last_name) AS full_name", "professor INNER JOIN meeting ON meeting.professor_id = professor.professor_id", "section_id = " + str(sections[i]["section_id"]))
        sections[i]["roster"] = SELECT_FROM_WHERE("DISTINCT(student.student_id), first_name, last_name, email, major", "student INNER JOIN enrollment on student.student_id=enrollment.student_id INNER JOIN section ON enrollment.section_id=section.section_id", "section.section_id=" + str(sections[i]["section_id"]))
        sections[i]["enrolled"] = len(sections[i]["roster"])
    return render_template('enrollment.html', page_title = "MyDashboard", courses=SELECT_FROM_WHERE("*", "course"), sections = sections, enrollments=list(map(lambda x: x["section_id"], SELECT_FROM_WHERE("*", "enrollment", "student_id=" + str(session['id'])))), id = session['id'], account_type = session.get('account_type'), user = SELECT_FROM_WHERE("*", session.get('account_type'), session.get('account_type') + "_id = " + str(session['id']))[0])

@application.route('/section/new')
def section_new():
    if not session.get('id') or not session.get('account_type'):
        return redirect('/')
    if session.get('account_type') == 'student':
        return redirect('/enroll')
    return render_template('section.html', courses = SELECT_FROM_WHERE("*", "course"), title = "Add Section", semesters = SELECT_FROM_WHERE("semester_id, CONCAT(season, ' ', LEFT(start_date, 4)) AS name", "semester"), professors = SELECT_FROM_WHERE("*", "professor", "1=1 ORDER BY last_name"), id = "null", user_id = session['id'], section=None, user = SELECT_FROM_WHERE("*", session.get('account_type'), session.get('account_type') + "_id = " + str(session['id']))[0])

@application.route('/section/<string:section_id>/edit')
def section_edit(section_id):
    if not session.get('id') or not session.get('account_type'):
        return redirect('/')
    if session.get('account_type') == 'student':
        return redirect('/enroll')
    if len(SELECT_FROM_WHERE("*", "meeting", "section_id=" + str(section_id) + " AND professor_id=" + str(session.get('id')))) == 0:
        return redirect('/dashboard')
    section = SELECT_FROM_WHERE("*", "section", "section_id=" + str(section_id))[0]
    section["meeting_times"] = SELECT_FROM_WHERE("day, CONCAT(start_time, '') AS start_time, CONCAT(end_time, '') AS end_time, room, professor_id", "meeting", "section_id = " + str(section_id))
    return render_template('section.html', id = section_id, section = section, courses = SELECT_FROM_WHERE("*", "course"), semesters = SELECT_FROM_WHERE("semester_id, CONCAT(season, ' ', LEFT(start_date, 4)) AS name", "semester"), professors = SELECT_FROM_WHERE("*", "professor", "1=1 ORDER BY last_name"), title = "Edit Section", user = SELECT_FROM_WHERE("*", session.get('account_type'), session.get('account_type') + "_id = " + str(session['id']))[0])

@application.route('/logout')
def logout():
    del session['id']
    del session['account_type']
    return {"message": "Logged out"}

@application.route('/revenue')
def revenue():
    return render_template('report.html', services=SELECT_FROM_WHERE("*", "service"))

@application.route("/revenue/download", methods=["GET", "POST"])
def revenue_download():
    total_revenue = SELECT_FROM_WHERE("*", "orders")
    total_revenue += [{"total_revenue":'${:,.2f}'.format(float(SELECT_FROM_WHERE("SUM(total) AS total_revenue", "orders")[0]["total_revenue"]))}]
    revenue_by_service = SELECT_FROM_WHERE("SUM(total) AS total, name, type, service.service_id", "orders RIGHT JOIN service ON orders.service_id=service.service_id", "1=1 GROUP BY service_id ORDER BY service_id")
    order_by_service = SELECT_FROM_WHERE("COUNT(*) AS count, name, type, service.service_id", "orders RIGHT JOIN service ON orders.service_id=service.service_id", "1=1 GROUP BY service_id ORDER BY service_id")
    order_by_service_by_month = SELECT_FROM_WHERE("*", "service")
    for order in order_by_service_by_month:
        order["orders_by_month"] = SELECT_FROM_WHERE("COUNT(*) as count, LEFT(date, 7) as month", "orders", "service_id=" + str(order["service_id"]) + " GROUP BY month")
    reports = {
        "total_revenue": total_revenue,
        "revenue_by_service": revenue_by_service,
        "order_by_service": order_by_service,
        "order_by_service_by_month": order_by_service_by_month
    }
    csv_data = generate_csv([["Total Revenue", SELECT_FROM_WHERE("CONCAT(SUM(total), '') AS total_revenue", "orders")[0]["total_revenue"]]])
    csv_data += generate_csv([[]])
    csv_data += generate_csv([["Revenue By Each Service"]])
    csv_data += generate_csv([["Service ID", "Service Type", "Service Name", "Revenue"]])
    for order in revenue_by_service:
        csv_data += generate_csv([[order["service_id"], order["type"], order["name"], order["total"] if order["total"] else 0]])
    csv_data += generate_csv([[]])
    csv_data += generate_csv([[]])
    csv_data += generate_csv([["Orders By Each Service"]])
    csv_data += generate_csv([["Service ID", "Service Type", "Service Name", "Orders"]])
    for order in order_by_service:
        csv_data += generate_csv([[order["service_id"], order["type"], order["name"], order["count"]]])
    csv_data += generate_csv([[]])
    csv_data += generate_csv([["Orders by each service by month"]])
    csv_data += generate_csv([["Service ID", "Service Type", "Service Name", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Sep", "Oct", "Nov", "Dec"]])
    values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for service in order_by_service_by_month:
        values_to_filter = list(map(lambda order: order["count"],service["orders_by_month"]))
        monthsToFilter = list(map(lambda order: int(order["month"].split("-")[1]),service["orders_by_month"]))
        for i in range(len(values_to_filter)):
            values[monthsToFilter[i] - 1] = values_to_filter[i]
        csv_data += generate_csv([[service["service_id"], service["type"], service["name"]] + values])
    match request.method:
        case 'GET':
            return Response(
                csv_data,
                mimetype='text/csv',
                headers={"Content-Disposition": "attachment;filename=EnrollMe_Report_As_Of_" + str(date.today()) + ".csv"}
            )
        case 'POST':
            return reports


@application.route('/ai', methods=['POST'])
def ai():
    body = request.json
    return {"response": generate_course(body.get('query'), body.get('currently_taking'))}

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True, port=8000)