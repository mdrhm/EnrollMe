CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    service_id INT,
    customer_id INT,
    total DECIMAL (10, 2),
    FOREIGN KEY (service_id) REFERENCES service(service_id)
    ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
    ON DELETE CASCADE
);
