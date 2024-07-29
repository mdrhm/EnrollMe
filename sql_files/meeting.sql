CREATE TABLE `meeting` (
  `meeting_id` int(11) NOT NULL,
  `section_id` int(11) DEFAULT NULL,
  `day` varchar(3) DEFAULT NULL,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  `professor_id` int(11) DEFAULT NULL,
  `room` varchar(50) DEFAULT NULL
);

ALTER TABLE `meeting`
  ADD PRIMARY KEY (`meeting_id`),
  ADD KEY `section_id` (`section_id`),
  ADD KEY `professor_id` (`professor_id`);

ALTER TABLE `meeting`
  MODIFY `meeting_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

ALTER TABLE `meeting`
  ADD CONSTRAINT `meeting_ibfk_1` FOREIGN KEY (`section_id`) REFERENCES `section` (`section_id`),
  ADD CONSTRAINT `meeting_ibfk_2` FOREIGN KEY (`professor_id`) REFERENCES `professor` (`professor_id`);
