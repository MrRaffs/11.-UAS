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
    category_name VARCHAR(255) NOT NULL UNIQUE
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
    FOREIGN KEY (destination_saving_id) REFERENCES savings(saving_id) ON DELETE SET NULL, -- Reference to savings table
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