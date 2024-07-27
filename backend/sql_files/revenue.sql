CREATE TABLE revenue (
    revenue_id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(255),
    source VARCHAR(255),
    amount DECIMAL(10, 2),
    description TEXT
);
