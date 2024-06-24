# API Docs

### Endpoint: `/get_courses`

### Parameters

- `q` (optional): A search query to filter courses by their subject, level, or name. This performs a partial match.
- `id` (optional): The course ID to filter the courses. This performs an exact match.

### Example Requests and Response

#### 1. Retrieve all courses

```http
GET /get_courses
```
#### Response
```json
[
  {
    "course_id": 1,
    "course_level": 10300,
    "course_subject": "CSC",
    "credits": 3,
    "name": "Introduction to Computing for Majors"
  },
  {
    "course_id": 2,
    "course_level": 10400,
    "course_subject": "CSC",
    "credits": 4,
    "name": "Discrete Mathematical Structures"
  },
  {
    "course_id": 3,
    "course_level": 11300,
    "course_subject": "CSC",
    "credits": 1,
    "name": "Programming Language"
  },
  {
    "course_id": 4,
    "course_level": 21100,
    "course_subject": "CSC",
    "credits": 3,
    "name": "Fundamentals of Computer Systems"
  },
  ...
]
```

#### 2. Retrieve a course by ID
```http
GET /get_courses?id=1
```
#### Response
```json
[
  {
    "course_id": 1,
    "course_level": 10300,
    "course_subject": "CSC",
    "credits": 3,
    "name": "Introduction to Computing for Majors"
  }
]
```

#### 3. Search for Courses
```http
GET /get_courses?q=intro
```
#### Response
```json
[
  {
    "course_id": 1,
    "course_level": 10300,
    "course_subject": "CSC",
    "credits": 3,
    "name": "Introduction to Computing for Majors"
  },
  {
    "course_id": 10,
    "course_level": 30400,
    "course_subject": "CSC",
    "credits": 3,
    "name": "Introduction to Theoretical Computer Science"
  },
  {
    "course_id": 14,
    "course_level": 33600,
    "course_subject": "CSC",
    "credits": 3,
    "name": "Introduction to Database Systems"
  },
  {
    "course_id": 24,
    "course_level": 48600,
    "course_subject": "CSC",
    "credits": 3,
    "name": "Introduction to Computational Complexity"
  }
]
```

### Endpoint: `/get_professors`

### Parameters

- `q` (optional): A search query to filter professors by their name. This performs a partial match.
- `id` (optional): The professor ID to filter the professors. This performs an exact match.

### Example Requests and Response

#### 1. Retrieve all professors

```http
GET /get_professors
```
#### Response
```json
[
  [
    {
      "email": "manshel@ccny.cuny.edu",
      "id": 1,
      "name": "Michael Anshel"
    },
    {
      "email": "aarapi@ccny.cuny.edu",
      "id": 2,
      "name": "Albi Arapi"
    },
    {
      "email": "hauda@ccny.cuny.edu",
      "id": 3,
      "name": "Hesham Auda"
    },
    {
      "email": "navteniev@ccny.cuny.edu",
      "id": 4,
      "name": "Nikolai Avteniev"
    },
    {
      "email": "obetancourt@ccny.cuny.edu",
      "id": 5,
      "name": "Octavio Betancourt"
    },
  ...
]
```

#### 2. Retrieve a professor by ID
```http
GET /get_professors?id=44
```
#### Response
```json
[
  {
    "email": "wskeith@ccny.cuny.edu",
    "id": 44,
    "name": "William Skeith"
  }
]
```

#### 3. Search for Professors
```http
GET /get_professors?q=au
```
#### Response
```json
[
  {
    "email": "hauda@ccny.cuny.edu",
    "id": 3,
    "name": "Hesham Auda"
  },
  {
    "email": "apedersen@cs.ccny.cuny.edu",
    "id": 40,
    "name": "Arthur Paul Pedersen"
  },
  {
    "email": "ctaylor2@ccny.cuny.edu",
    "id": 47,
    "name": "Chaunce  Taylor"
  }
]
```