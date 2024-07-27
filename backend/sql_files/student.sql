CREATE TABLE `student` (
  `student_id` int(11) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone_number` varchar(50) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `sex` char(1) DEFAULT NULL,
  `major` char(3) DEFAULT NULL
);

ALTER TABLE `student`
  ADD PRIMARY KEY (`student_id`);

ALTER TABLE `student`
  MODIFY `student_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10000000;