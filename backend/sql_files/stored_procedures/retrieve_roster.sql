DELIMITER //

CREATE PROCEDURE RetrieveRoster (
	IN p_professor_id INT,
    	IN p_section_id INT
)

BEGIN

	SELECT DISTINCT student.student_id, student.first_name, student.last_name, student.email, student.major
	FROM student
	JOIN enrollment ON student.student_id = enrollment.student_id
	JOIN section ON section.section_id = enrollment.section_id
	JOIN meeting ON meeting.section_id = section.section_id
	JOIN professor ON meeting.professor_id = professor.professor_id
	WHERE professor.professor_id = p_professor_id
    	AND enrollment.section_id = p_section_id
    	ORDER BY student.last_name, student.first_name;

END //

DELIMITER ;
