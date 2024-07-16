CREATE TABLE login (
    login_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT UNIQUE,
    professor_id INT UNIQUE,
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
  
    -- Make sure a user can't have both a student & professor ID
    CHECK ((student_id IS NOT NULL
        AND professor_id IS NULL)
        OR (student_id IS NULL
        AND professor_id IS NOT NULL))
);
