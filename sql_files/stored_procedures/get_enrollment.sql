DELIMITER //

CREATE PROCEDURE GetEnrollments(id INT)
BEGIN

SELECT DISTINCT
    (section.section_id),
    course.name AS course_name,
    section.course_id,
    course.credits,
    course.description,
    CONCAT(subject, ' ', course.course_level) AS course_code,
    semester.end_date,
    section.instruction_mode,
    semester.start_date,
    section.max_capacity,
    CONCAT(semester.season,
            ' ',
            LEFT(semester.start_date, 4)) AS semester
FROM
    course
        INNER JOIN
    section ON course.course_id = section.course_id
        INNER JOIN
    enrollment ON enrollment.section_id = section.section_id
        INNER JOIN
    semester ON section.semester_id = semester.semester_id
WHERE
    enrollment.student_id = id;

END //

DELIMITER ;
