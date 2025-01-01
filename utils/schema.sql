-- Table for Savings Categories (e.g., Bank BRI, Bank BCA, Cash)
CREATE TABLE savings_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL UNIQUE
);

-- Table for Savings (e.g., specific accounts linked to categories)
CREATE TABLE savings (
    saving_id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT,
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES savings_categories(category_id)
);

-- Table for Transaction Categories (e.g., Food, Home, Transport)
CREATE TABLE transaction_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL UNIQUE,
    category_type ENUM('expense','income') NOT NULL
);

-- Table for Transactions
CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    saving_id INT, -- Source saving account
    destination_saving_id INT DEFAULT NULL, -- Destination saving account for transfers
    category_id INT DEFAULT NULL, -- For income/expense transactions
    transaction_type ENUM('income', 'expense', 'transfer') NOT NULL,
    transaction_date DATE NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    notes TEXT,
    FOREIGN KEY (saving_id) REFERENCES savings(saving_id),
    FOREIGN KEY (destination_saving_id) REFERENCES savings(saving_id),
    FOREIGN KEY (category_id) REFERENCES transaction_categories(category_id)
);

-- Query to fetch all transactions with foreign keys replaced by corresponding names
SELECT 
    t.transaction_id,
    t.saving_id,
    s1.category_id AS source_category_id,
    sc1.category_name AS source_category_name,
    t.destination_saving_id,
    s2.category_id AS destination_category_id,
    sc2.category_name AS destination_category_name,
    tc.category_id AS transaction_category_id,
    tc.category_name AS transaction_category_name,
    t.transaction_type,
    t.transaction_date,
    t.amount,
    t.notes
FROM 
    transactions t
-- Join to get source saving account details
LEFT JOIN 
    savings s1 ON t.saving_id = s1.saving_id
LEFT JOIN
    savings_categories sc1 ON s1.category_id = sc1.category_id
-- Join to get destination saving account details
LEFT JOIN 
    savings s2 ON t.destination_saving_id = s2.saving_id
LEFT JOIN 
    savings_categories sc2 ON s2.category_id = sc2.category_id
-- Join to get transaction category details
LEFT JOIN 
    transaction_categories tc ON t.category_id = tc.category_id;







-- Insert dummy data into savings_categories
INSERT INTO savings_categories (category_name) VALUES 
('Bank BRI'), 
('Cash');

-- Insert dummy data into savings
INSERT INTO savings (category_id, balance) VALUES 
(1, 7000000), 
(2, 2000000);

-- Insert dummy data into transaction_categories
INSERT INTO transaction_categories (category_name, category_type) VALUES 
('Bills', 'expense'), 
('Transportation', 'expense'), 
('Home', 'expense'), 
('Electronics', 'expense'), 
('Education', 'expense'), 
('Entertainment', 'expense'), 
('Food', 'expense'), 
('Shopping', 'expense'), 
('Telephone', 'expense'), 
('Grants', 'income'), 
('Sale', 'income'), 
('Salary', 'income');

-- Insert dummy data into transactions
INSERT INTO transactions (saving_id, destination_saving_id, category_id, transaction_type, transaction_date, amount, notes) VALUES 
(1, NULL, 1, 'expense', '2024-10-01', 500000, 'Monthly bills'), 
(1, NULL, 2, 'expense', '2024-10-05', 200000, 'Bus fare'), 
(1, NULL, 3, 'expense', '2024-10-10', 1000000, 'Home maintenance'), 
(2, NULL, 2, 'expense', '2024-10-16', 50000, 'Cash payment for transportation'), 
(1, NULL, 5, 'expense', '2024-10-20', 300000, 'School fees'), 
(1, NULL, 6, 'expense', '2024-10-25', 250000, 'Movie tickets'), 
(1, NULL, 7, 'expense', '2024-10-30', 500000, 'Groceries'), 
(1, NULL, 8, 'expense', '2024-11-01', 1000000, 'Clothes shopping'), 
(1, NULL, 9, 'expense', '2024-11-05', 150000, 'Phone bill'), 
(1, NULL, 10, 'income', '2024-11-10', 2000000, 'Grant received'), 
(1, NULL, 11, 'income', '2024-11-15', 3000000, 'Item sold'), 
(1, NULL, 12, 'income', '2024-11-20', 5000000, 'Monthly salary'), 
(1, NULL, 1, 'expense', '2024-11-25', 500000, 'Monthly bills'), 
(1, NULL, 2, 'expense', '2024-11-30', 200000, 'Bus fare'), 
(1, NULL, 3, 'expense', '2024-12-01', 1000000, 'Home maintenance'), 
(1, NULL, 4, 'expense', '2024-12-05', 1500000, 'New phone'), 
(2, NULL, 7, 'expense', '2024-12-06', 150000, 'Cash payment for groceries'), 
(1, NULL, 5, 'expense', '2024-12-10', 300000, 'School fees'), 
(1, NULL, 6, 'expense', '2024-12-15', 250000, 'Movie tickets'), 
(2, NULL, 2, 'expense', '2024-12-16', 50000, 'Cash payment for transportation'), 
(1, NULL, 7, 'expense', '2024-12-20', 500000, 'Groceries'), 
(1, NULL, 8, 'expense', '2024-12-25', 1000000, 'Clothes shopping'), 
(1, NULL, 9, 'expense', '2024-12-30', 150000, 'Phone bill'), 
(1, 2, NULL, 'transfer', '2024-12-31', 1000000, 'Cashed out');