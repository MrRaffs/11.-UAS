
-- Table for Savings (e.g., specific accounts linked to categories)
CREATE TABLE IF NOT EXISTS savings (
    saving_id INT AUTO_INCREMENT PRIMARY KEY,
    saving_name VARCHAR(255) NOT NULL UNIQUE,
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0
);

-- Table for Transaction Categories (e.g., Food, Home, Transport)
CREATE TABLE IF NOT EXISTS transaction_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL UNIQUE,
    category_type ENUM('expense','income') NOT NULL
);

-- Table for Transactions
CREATE TABLE IF NOT EXISTS transactions (
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


