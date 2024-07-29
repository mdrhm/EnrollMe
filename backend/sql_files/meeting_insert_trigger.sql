DROP TRIGGER before_meeting_insert;

DELIMITER //

CREATE TRIGGER before_meeting_insert
BEFORE INSERT ON meeting
FOR EACH ROW
BEGIN
	
    -- Declare variables
    DECLARE schedule_conflict_exists BOOL DEFAULT FALSE;
    DECLARE room_conflict_exists BOOL DEFAULT FALSE;
    DECLARE new_semester_id INT DEFAULT NULL;
    
    SELECT semester_id
    INTO new_semester_id
    FROM section
    WHERE section_id = NEW.section_id;
    
    
    -- Verify no scheduling conflicts
    IF EXISTS(
		SELECT 1
        FROM meeting
        JOIN section ON section.section_id = meeting.section_id
        WHERE meeting.professor_id = NEW.professor_id
			AND section.semester_id = new_semester_id
			AND meeting.day = NEW.day
			  AND (
				(meeting.start_time < NEW.end_time AND meeting.end_time > NEW.start_time)
		  ) 	 
    ) THEN SET schedule_conflict_exists = TRUE;
    END IF;
    
	IF schedule_conflict_exists THEN
	SIGNAL SQLSTATE '45000'
	SET MESSAGE_TEXT = 'Scheduling conflict detected for the professor';
    END IF;    
    
    -- Verify no room conflicts
    IF EXISTS(
		SELECT 1
        FROM meeting
        JOIN section ON section.section_id = meeting.section_id
        WHERE meeting.room = NEW.room
			AND section.semester_id = new_semester_id
			AND meeting.day = NEW.day
			  AND (
				(meeting.start_time < NEW.end_time AND meeting.end_time > NEW.start_time)
		  ) 	 
    ) THEN SET room_conflict_exists = TRUE;
    END IF;
    
	IF room_conflict_exists THEN
	SIGNAL SQLSTATE '45000'
	SET MESSAGE_TEXT = 'The requested room is already in use.';
    END IF;
    
END //

DELIMITER ;
