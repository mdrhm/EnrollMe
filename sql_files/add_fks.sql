ALTER TABLE enrollment
ADD FOREIGN KEY (section_id) REFERENCES section(section_id)
ON DELETE CASCADE,
ADD FOREIGN KEY (student_id) REFERENCES student(student_id)
ON DELETE CASCADE;

ALTER TABLE section
ADD FOREIGN KEY (course_id) REFERENCES course(course_id)
ON DELETE CASCADE,
ADD FOREIGN KEY (professor_id) REFERENCES professor(professor_id)
ON DELETE CASCADE;

ALTER TABLE login
ADD FOREIGN KEY (student_id) REFERENCES student (student_id)
ON DELETE CASCADE,
ADD FOREIGN KEY (professor_id) REFERENCES professor (professor_id)
ON DELETE CASCADE;
