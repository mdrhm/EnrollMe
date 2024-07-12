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
    "last_name": "Doe", 
    "email": "john.doe@example.com", 
    "phone_number": "1234567890",
    "department": "CSC", 
    "password": "securepassword" 
 }
```
`DELETE /professors` 
Delete a professor.

**Request Body (JSON):**
- `id`: The ID of the professor to be deleted.

**Responses:**
- `200 OK`: A JSON object with a success message.
- `400 Bad Request`: A JSON object with an error message if the `id` header is missing.

**Example:**
```
DELETE /professors
Body: { 
    "id": "10000" 
}
```

### Students

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
    "first_name": "Jane", 
    "last_name": "Doe", "email": 
    "jane.doe@example.com", 
    "phone_number": "0987654321", 
    "dob": "1995-05-05", 
    "sex": "F", 
    "major": "CSC", 
    "password": "securepassword" 
}
```

`DELETE /students`
Delete a student.

#### DELETE /students
Delete a student.

**Request Body (JSON):**
- `id`: The ID of the student to be deleted.

**Responses:**
- `200 OK`: A JSON object with a success message.
- `400 Bad Request`: A JSON object with an error message if the `id` field is missing.

**Example:**
```
DELETE /students
Body: { 
    "id": "1" 
}
```

### Login

`GET /login`
Authenticate a user (student or professor).

**Request Body (JSON):**
- `id` (optional): The ID of the user.
- `password`: The password of the user.
- `email` (optional): The email of the user.
- `account_type`: The type of account (`student` or `professor`).

**Responses:**
- `200 OK`: A JSON object of the authenticated user.
- `400 Bad Request`: A JSON object with an error message if required fields are missing.
- `401 Unauthorized`: A JSON object with an error message if login credentials are invalid.

**Example:**
```
GET /login
Body: { 
    "email": "jane.doe@example.com", 
    "password": "securepassword", 
    "account_type": "student" 
}
```
