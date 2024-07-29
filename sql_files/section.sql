CREATE TABLE `section` (
  `course_id` int(11) DEFAULT NULL,
  `section_id` int(11) NOT NULL DEFAULT '0',
  `instruction_mode` varchar(20) DEFAULT NULL,
  `max_capacity` int(11) DEFAULT NULL,
  `semester_id` int(11) DEFAULT NULL
);

ALTER TABLE `section`
  ADD PRIMARY KEY (`section_id`),
  ADD KEY `course_id` (`course_id`),
  ADD KEY `semester_id` (`semester_id`),
    MODIFY `section_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1000;

ALTER TABLE `section`
  ADD CONSTRAINT `section_ibfk_1` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `section_ibfk_3` FOREIGN KEY (`semester_id`) REFERENCES `semester` (`semester_id`);
