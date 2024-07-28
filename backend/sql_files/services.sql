CREATE TABLE service (
    service_id INT PRIMARY KEY AUTO_INCREMENT,
	type VARCHAR(255),  -- School-wide License, Education Advertising, Job Forum Advertising
    name VARCHAR(255), 	-- Targeted ad, Regualar ad, Small school license, Medium school license, Large school license
	price DECIMAL(10, 2),
    description TEXT
);


INSERT INTO service (type, name, description, price) VALUES 
('License', 'Small school License', 'A school wide license for schools with less than 5000 students', 10000.00),
('License', 'Medium school License', 'A school wide license for schools with 5000 - 15000 students', 20000.00),
('License', 'Large school License', 'A school wide license for schools with more than 15000 students', 30000.00),
('Educational Resource Advertising', 'Targeted Impression', 'An ad displaying an educational aid shown to students based on enrolled courses and/or GPA', 1.50),
('Education Resource Advertising', 'Regular Impression', 'An ad displaying an educational aid shown to students', .75),
('Job Forum Advertising', 'Targeted Impression', 'An ad displaying an job/internship opportunity shown to students based on enrolled courses/course history and/or GPA', 1.00),
('Job Forum Advertising', 'Regular Impression', 'An ad displaying an job/internship opportunity shown to students', .50),
('Education Instituion Advertising', 'Targeted Impression', 'An ad displaying an educational institution shown to students', 2.00),
('Education Institution Advertising', 'Regular Impression', 'An ad displaying an educational institution shown to students based on major and/or GPA', 1.00);
