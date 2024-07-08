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

### Professors

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

**Headers:**
- `firstname`: First name of the professor.
- `lastname`: Last name of the professor.
- `email`: Email of the professor.
- `number`: Phone number of the professor.
- `department`: Department of the professor.
- `password`: Password for the professor's login.

**Responses:**
- `201 Created`: A JSON object of the created professor.
- `400 Bad Request`: A JSON object with an error message if any required header is missing.

**Example:**
```
POST /professors
Headers: firstname=John,
lastname=Doe,
email=john.doe@example.com,
number=1234567890,
department=Math,
password=securepassword
```

`DELETE /professors` 
Delete a professor.

**Headers:**
- `id`: The ID of the professor to be deleted.

**Responses:**
- `200 OK`: A JSON object with a success message.
- `400 Bad Request`: A JSON object with an error message if the `id` header is missing.

**Example:**
```
DELETE /professors
Headers: id=100000
```

### Students

`POST /students`
Add a new student.

**Headers:**
- `firstname`: First name of the student.
- `lastname`: Last name of the student.
- `email`: Email of the student.
- `number`: Phone number of the student.
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
Headers: firstname=Jane, 
lastname=Doe, 
email=jane.doe@example.com, 
number=0987654321, 
dob=1995-05-05, 
sex=F, 
major=CSC, 
password=securepassword
```

`DELETE /students`
Delete a student.

**Headers:**
- `id`: The ID of the student to be deleted.

**Responses:**
- `200 OK`: A JSON object with a success message.
- `400 Bad Request`: A JSON object with an error message if the `id` header is missing.

**Responses:**
- `200 OK`: A JSON object with a success message.
- `400 Bad Request`: A JSON object with an error message if the `id` header is missing.

**Example:**
```
DELETE /students
Headers: id=10000000
```

### Login

`GET /login`
Authenticate a user (student or professor).

**Headers:**
- `id` (optional): The ID of the user.
- `password`: The password of the user.
- `email` (optional): The email of the user.
- `accounttype`: The type of account (`student` or `professor`).

**Responses:**
- `200 OK`: A JSON object of the authenticated user.
- `400 Bad Request`: A JSON object with an error message if required headers are missing.
- `401 Unauthorized`: A JSON object with an error message if login credentials are invalid.

**Example:**
```
GET /login
Headers: email=jane.doe@example.com, 
password=securepassword, 
accounttype=student
```
