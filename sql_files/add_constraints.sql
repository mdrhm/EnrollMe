ALTER TABLE section
ADD CONSTRAINT valid_time CHECK(start_time < end_time),
ADD CONSTRAINT online_class CHECK(instruction_mode <> 'online' OR room IS NULL);

ALTER TABLE semester
ADD CONSTRAINT valid_date CHECK(start_date < end_date);
