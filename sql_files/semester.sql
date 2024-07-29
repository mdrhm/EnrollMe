CREATE TABLE `semester` (
  `semester_id` int(11) NOT NULL,
  `season` varchar(255) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL
);

ALTER TABLE `semester`
  ADD PRIMARY KEY (`semester_id`);

ALTER TABLE `semester`
  MODIFY `semester_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;COMMIT;

INSERT INTO `semester` (`semester_id`, `season`, `year`, `start_date`, `end_date`) VALUES
    (1, 'Fall', 2024, '2024-08-28', '2024-12-21');