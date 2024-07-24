DELIMITER //

CREATE PROCEDURE EnrollStudent (
	IN p_student_id INT,
    IN p_section_id INT,
    OUT p_status VARCHAR(255)
)
proc: BEGIN
    -- Declare variables
    DECLARE already_enrolled BOOL DEFAULT FALSE;
    DECLARE conflict_exists BOOL DEFAULT FALSE;
    DECLARE total_credits INT DEFAULT 0;
    DECLARE filled_seats INT DEFAULT 0;
    DECLARE capacity INT DEFAULT 0;
    
    DECLARE new_semester_id INT DEFAULT 0;
    DECLARE new_course_id INT DEFAULT 0;
    DECLARE new_credits TIME DEFAULT NULL;    
    
    
    SELECT section.semester_id, section.course_id, course.credits
    INTO new_semester_id, new_course_id, new_credits
    FROM section 
    JOIN course ON section.course_id = course.course_id
    JOIN semester ON semester.semester_id = section.semester_id
    WHERE section.section_id = P_section_id;
    
    -- Verify student isn't already enrolled in course (checks semester so they can enroll in a future semester if they fail)
    IF EXISTS(
		SELECT 1
		FROM enrollment
		JOIN section ON enrollment.section_id = section.section_id
		WHERE enrollment.student_id = p_student_id
		  AND section.course_id = new_course_id
          AND section.semester_id = new_semester_id
          
    ) THEN SET already_enrolled = TRUE;
    END IF;
    
    IF already_enrolled THEN
		SET p_status = 'Duplicate course error: You are already enrolled in this course';
        LEAVE proc;
    END IF;
    
    
    -- Verify that the class still has space
	SELECT COUNT(*) INTO filled_seats
	FROM enrollment
	WHERE section_id = p_section_id;
		
	SELECT max_capacity INTO capacity 
	FROM section
	WHERE section_id = p_section_id;
    
    IF filled_seats >= capacity THEN
		SET p_status = 'Class full: There are no more available seats for this course';
        LEAVE proc;
    END IF;
    
    
    -- Verify enrolling won't put student over 17 credit limit
	SELECT SUM(course.credits)
	INTO total_credits 
	FROM course
	JOIN section ON course.course_id = section.course_id
	JOIN enrollment ON enrollment.section_id = section.section_id
	WHERE enrollment.student_id = p_student_id
    AND section.semester_id = new_semester_id;

    SET total_credits = total_credits + new_credits;

    IF total_credits > 17 THEN
        SET p_status = 'Credit limit exceeded: total credits cannot exceed 17';
        LEAVE proc;
    END IF;
    
    
    -- Verify no scheduling conflicts
    IF EXISTS(
		SELECT 1
        FROM enrollment
		JOIN section ON enrollment.section_id = section.section_id
        JOIN meeting m1 ON m1.section_id = section.section_id
		JOIN meeting m2 ON m2.section_id = p_section_id
		WHERE enrollment.student_id = p_student_id
		  AND section.semester_id = new_semester_id
          AND m1.day = m2.day
		  AND (
			(m1.start_time < m2.end_time AND m1.end_time > m2.start_time)
      ) 
    ) THEN SET conflict_exists = TRUE;
    END IF;
    
	IF conflict_exists THEN
		SET p_status = 'Scheduling conflict detected for the student.';
        LEAVE proc;
    END IF;
    
    INSERT INTO enrollment (student_id, section_id) 
    VALUES (p_student_id, p_section_id);
    SET p_status = 'Enrollment Successful';
    
END //

DELIMITER ;


