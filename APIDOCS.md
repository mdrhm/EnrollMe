# Endpoints

## Courses

`GET /courses`
Retrieve a list of courses.

**Parameters:**
- `q` (optional): A search query to filter courses by concatenated `subject`, `course_level`, and `name`.
- `id` (optional): The ID of a specific course.

**Responses:**
- `200 OK`: A JSON array of course objects.

**Examples:**
```
GET /courses
GET /courses?id=1
GET /courses?q=intro
```

`POST /courses`
Add a new course.

**Request Body (JSON):**
- `subject`: The subject of the course.
- `course_level`: The level of the course.
- `name`: The name of the course.
- `credits`: The amount of credits the course is worth.
- `description`: The description of the course.

**Responses:**
- `201 Created`: A JSON object of the created course.

**Examples:**
```
POST /courses
Body: { 
{
    "subject":"BIO",
    "course_level": 10100,
    "name": "Biological Foundations I",
    "credits": 4,
    "description": "Introduction to biology, emphasizing primarily the cell and molecular levels of organization. Topics include characteristics of life, cellular organization and diversity, chemistry of life, bioenergetics, reproduction and early development, and major living groups. The course features in-depth study of selected topics that are foundational for upper level study. Students develop critical thinking and technical skills that are essential for mastering the content areas and being successful in upper level courses. These include: vocabulary skills, critical thinking, collaborative learning, microscopy, collection and handling of scientific data, and elements of scientific investigation."
}
```

`DELETE /courses`
Delete a course.

**Request Body (JSON):**
- `course_id`: The ID of the course to be deleted.

**Responses:**
- `200 OK`: A JSON object with a success message.
- `400 Bad Request`: A JSON object with an error message if the `course_id` is missing.

**Examples:**
```
DELETE /courses
Body: { 
    "course_id": "1" 
}
```

`PUT /courses`
Update a course.

**Request Body (JSON):**
- `course_id` (required): The ID of the course to be updated
- Details that need to be updated such as `subject`, `course_level`, `name`, `credits`, `description`.

**Responses:**
- `200 OK`: A JSON object of the updated course.
- `400 Bad Request`: A JSON object with an error message if the `course_id` is missing.

**Examples:**
```
PUT /courses
Body: {
    "course_id": 39,
    "subject":"BIO",
    "course_level": 10200,
    "name": "Biological Foundations II",
    "credits": 4,
    "description": "Second semester of introductory biology, emphasizing organismic biology, evolution, and ecology. Topics include heredity, macro- and microevolution, structure and function of body systems, and ecology. The course features a survey of topics in lecture and in-depth study of selected topics in laboratories and workshops. Students develop critical thinking and technical skills that are essential for mastering the content areas and being successful in further study. These include: vocabulary skills, problem solving, collaborative learning, computer skills, experimental design, collection and analysis of scientific data, and preparing scientific reports."
}
```

## Sections

`GET /sections`
Retrieve a list of sections.

**Parameters:**
- `section` (optional): The ID of a specific section.
- `course` (optional): The ID of a course to filter sections by.
- `professor` (optional): The ID of a professor to filter sections by.

**Responses:**
- `200 OK`: A JSON array of section objects, each including nested `days`, `rooms`, and `professors`.

**Examples:**
```
GET /sections
GET /sections?course=1
GET /sections?professor=100000
```

`POST /sections`
Add a new section.

**Request Body (JSON):**
- `course_id`: The ID of the course associated with the section.
- `meeting_times`: An array of objects describing what days the section will meet.
- `instruction_mode`: The mode of which the section will meet (`In Person`, `Hybrid Synchronous`, `Online`)
- `max_capacity`: The number of students that can enroll into the section
- `semester_id`: The ID of the semester that the section will take place


**Responses:**
- `201 Created`: A JSON object of the created section.

**Examples:**
```
POST /sections
Body: {
    "course_id": 2,
    "meeting_times": [
        {
            "day":"Fri",
            "start_time":"9:00:00",
            "end_time":"10:40:00",
            "professor_id": 10009,
            "room": "NAC 6/123"
        },
        {
            "day":"Mon",
            "start_time":"14:00:00",
            "end_time":"15:40:00",
            "professor_id": 10010,
            "room": "Marshak MR1"
        },
        {
            "day":"Wed",
            "start_time":"14:00:00",
            "end_time":"15:40:00",
            "professor_id": 10010,
            "room": "Marshak MR1"
        }
    ],
    "instruction_mode": "In Person",
    "max_capacity": 30,
    "semester_id": 1
}
```

`DELETE /sections`
Delete a section.

**Request Body (JSON):**
- `section_id`: The ID of the section to be deleted.

**Responses:**
- `200 OK`: A JSON object with a success message.
- `400 Bad Request`: A JSON object with an error message if the `section_id` is missing.

**Examples:**
```
DELETE /sections
Body: { 
    "section_id": "1000" 
   }
```

`PUT /sections`
Update a section.

**Request Body (JSON):**
- `section_id` (required): The ID of the section to be updated
- Details of the section to be updated such as `course_id`, `meeting_times`, `instruction_mode`, `max_capacity`, `semester_id`

**Responses:**
- `200 OK`: A JSON object of the updated section.
- `400 Bad Request`: A JSON object with an error message if the `section_id` is missing.

**Examples:**
```
PUT /sections
Body: {
    "section": 1000,
    "course_id": 2,
    "meeting_times": [
        {
            "day":"Fri",
            "start_time":"9:00:00",
            "end_time":"10:40:00",
            "professor_id": 10009,
            "room": "NAC 6/123"
        },
        {
            "day":"Mon",
            "start_time":"14:00:00",
            "end_time":"15:40:00",
            "professor_id": 10010,
            "room": "Marshak MR1"
        },
        {
            "day":"Wed",
            "start_time":"14:00:00",
            "end_time":"15:40:00",
            "professor_id": 10010,
            "room": "Marshak MR1"
        }
    ],
    "instruction_mode": "In Person",
    "max_capacity": 30,
    "semester_id": 1
}
```

## Professors

`GET /professors`
Retrieve a list of professors.

**Parameters:**
- `q` (optional): A search query to filter professors by their full name.
- `id` (optional): The ID of a specific professor.

**Responses:**
- `200 OK`: A JSON array of professor objects.

**Examples:**
```
GET /professors
GET /professors?id=100000
GET /professors?q=John
```

`POST /professors`
Add a new professor.

**Request Body (JSON):**
- `first_name`: First name of the professor.
- `last_name`: Last name of the professor.
- `email`: Email of the professor.
- `phone_number`: Phone number of the professor.
- `department`: Department of the professor.
- `password`: Password for the professor's login.

**Responses:**
- `201 Created`: A JSON object of the created professor.
- `400 Bad Request`: A JSON object with an error message if any required header is missing.

**Example:**
```
POST /professors
Body: {
    "first_name": "John",
    "last_name": "Smith",
    "email": "johnsmith@ccny.cuny.edu",
    "phone_number": "718-920-8001",
    "department": "CSC",
    "password": "hello123"
}
```

`DELETE /professors`
Delete a professor.

**Request Body (JSON):**
- `professor_id`: The ID of the professor to be deleted.

**Responses:**
- `200 OK`: A JSON object with a success message.
- `400 Bad Request`: A JSON object with an error message if the `professor_id` is missing.

**Example:**
```
DELETE /professors
Body: {
    "professor_id": "10000"
}
```

`PUT /professors`
Update a professor.

**Request Body (JSON):**
- `professor_id` (required): The ID of the professor to be updated
- Details of the professor to be updated such as `first_name`, `last_name`, `email`, `phone_number`, `department`
- `old_password` and `new_password` if user wants to change password

**Responses:**
- `200 OK`: A JSON object of the updated professor.
- `400 Bad Request`: A JSON object with an error message if the `professor_id` is missing.

**Examples:**
```
PUT /professors
Body: {
    "professor_id": 10006,
    "first_name": "John",
    "last_name": "Smith",
    "email": "johnsmith@ccny.cuny.edu",
    "phone_number": "718-920-8001",
    "department": "CSC",
    "old_password": "hello123",
    "new_password": "test1234"
}
```

## Students

`POST /students`
Add a new student.

**Request Body (JSON):**
- `first_name`: First name of the student.
- `last_name`: Last name of the student.
- `email`: Email of the student.
- `phone_number`: Phone number of the student.
- `dob`: Date of birth of the student.
- `sex`: Sex of the student.
- `major`: Major of the student.
- `password`: Password for the student's login.

**Responses:**
- `201 Created`: A JSON object of the created student.
- `400 Bad Request`: A JSON object with an error message if any required header is missing.

**Example:**
```
POST /students
Body: {
    "first_name":"Maria",
    "last_name":"Johnson",
    "email":"mariajohnson@ccny.cuny.edu",
    "phone_number":"718-574-2723",
    "dob":"2004-05-30",
    "sex":"F",
    "major":"CSC",
    "password":"hello123"
}
```

`DELETE /students`
Delete a student.

**Request Body (JSON):**
- `student_id`: The ID of the student to be deleted.

**Responses:**
- `200 OK`: A JSON object with a success message.
- `400 Bad Request`: A JSON object with an error message if the `student_id` is missing.

**Examples:**
```
DELETE /students
Body: {
    "student_id": "10000000"
}
```

`PUT /students`
Update a student.

**Request Body (JSON):**
- `student_id` (required): The ID of the professor to be updated
- Details of the professor to be updated such as - `first_name`, `last_name`, `email`, `phone_number`, `dob`, `sex`, `major`
- `old_password` and `new_password` if user wants to change password

**Responses:**
- `200 OK`: A JSON object of the updated student.
- `400 Bad Request`: A JSON object with an error message if the `student_id` is missing.

**Examples:**
```
PUT /students
Body: {
    "student_id": 10000001,
>>>>>>> main
    "first_name":"Maria",
    "last_name":"Johnson",
    "email":"mariajohnson@ccny.cuny.edu",
    "phone_number":"7185742723",
    "dob":"2004-05-30",
    "sex":"F",
    "major":"CSC",
    "old_password": "test1234",
    "new_password": "hello123"

}
```

## Login

`POST /login`
Authenticate a user (student or professor).

**Request Body (JSON):**
- `username`: The ID or email of the user.
- `password`: The password of the user.
- `account_type`: The type of account (`student` or `professor`).

**Responses:**
- `200 OK`: A JSON object of the authenticated user.
- `400 Bad Request`: A JSON object with an error message if required fields are missing.
- `401 Unauthorized`: A JSON object with an error message if login credentials are invalid.

**Examples:**
```
POST /login
Body: {
    "username": "mariajohnson@ccny.cuny.edu",
    "password": "hello123",
    "account_type": "student"
}
```

## Enrollments

`GET /enrollments`
Retrieve a student's schedule.

**Parameters:**
- `id`: The ID of the student.

**Responses:**
- `200 OK`: A JSON array of the student's schedule.
- `400 Bad Request`: A JSON object with an error message if the `id` is missing.

**Examples:**
```
GET /enrollments?id=10000006
```

`POST /enrollments`
Add a new enrollment.

**Request Body (JSON):**
- `student_id`: The ID of the student.
- `section_id`: The ID of the section.

**Responses:**
- `201 Created`: A JSON object of the created student.
- `400 Bad Request`: A JSON object with an error message if any required header is missing.

**Example:**
```
POST /enrollments
Body: {
    "student_id": 10000006,
    "section_id": 1000
}
```
`DELETE /enrollments`
Delete an enrollment.

**Request Body (JSON):**
- `student_id`: The ID of the student associated with the enrollment.
- `section_id`: The ID of the section associated with the enrollment.

**Responses:**
- `200 OK`: A JSON object with a success message.
- `400 Bad Request`: A JSON object with an error message if the `student_id` is missing.

**Examples:**
```
DELETE /enrollments
Body: {
    "student_id": 10000006,
    "section_id": 1000
}
```

`PUT /enrollments`
Perform a mass update on a student's enrollments. This process will remove all previous enrollments that are not listed in the sections array. It will also enroll the student in any `sections` included in the `sections` array that they were not previously enrolled in.

**Request Body (JSON):**
- `student_id`: The ID of the student to update enrollments for.
- `sections`: An array of all section ID's is enrolled in.

**Responses:**
- `200 OK`: A JSON object of the updated enrollments.
- `400 Bad Request`: A JSON object with an error message if the `student_id` is missing.

**Examples:**
```
PUT /enrollments
Body: {
    "student_id": 10000006,
    "sections": [
        1000,
        1001
    ]
}
```

## Download Roster

`GET /roster`
Download a professor's roster

**Parameters:**
- `professor`: The ID of the professor.
- `section`: The ID of the section.

**Responses:**
- `200 OK`: A CSV file of the students enrolled in the professor's class.
- `400 Bad Request`: A JSON object with an error message if the `id` is missing.

**Examples:**
```
GET /roster?id=10014
```