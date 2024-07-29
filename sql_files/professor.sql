CREATE TABLE `professor` (
  `professor_id` int(11) NOT NULL,
  `first_name` varchar(50) DEFAULT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `department` varchar(5) DEFAULT NULL
);

ALTER TABLE `professor`
  ADD PRIMARY KEY (`professor_id`);

ALTER TABLE `professor`
  MODIFY `professor_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10000;
