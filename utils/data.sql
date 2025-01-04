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

-- -- Insert dummy data into savings
-- INSERT INTO savings (saving_name, balance) VALUES 
-- ('Bank BRI', 7000000), 
-- ('Cash', 2000000);

-- -- Insert dummy data into transactions
-- INSERT INTO transactions (saving_id, destination_saving_id, category_id, transaction_type, transaction_date, amount, notes) VALUES 
-- (1, NULL, 1, 'expense', '2024-10-01', 500000, 'Monthly bills'), 
-- (1, NULL, 2, 'expense', '2024-10-05', 200000, 'Bus fare'), 
-- (1, NULL, 3, 'expense', '2024-10-10', 1000000, 'Home maintenance'), 
-- (2, NULL, 2, 'expense', '2024-10-16', 50000, 'Cash payment for transportation'), 
-- (1, NULL, 5, 'expense', '2024-10-20', 300000, 'School fees'), 
-- (1, NULL, 6, 'expense', '2024-10-25', 250000, 'Movie tickets'), 
-- (1, NULL, 7, 'expense', '2024-10-30', 500000, 'Groceries'), 
-- (1, NULL, 8, 'expense', '2024-11-01', 1000000, 'Clothes shopping'), 
-- (1, NULL, 9, 'expense', '2024-11-05', 150000, 'Phone bill'), 
-- (1, NULL, 10, 'income', '2024-11-10', 2000000, 'Grant received'), 
-- (1, NULL, 11, 'income', '2024-11-15', 3000000, 'Item sold'), 
-- (1, NULL, 12, 'income', '2024-11-20', 5000000, 'Monthly salary'), 
-- (1, NULL, 1, 'expense', '2024-11-25', 500000, 'Monthly bills'), 
-- (1, NULL, 2, 'expense', '2024-11-30', 200000, 'Bus fare'), 
-- (1, NULL, 3, 'expense', '2024-12-01', 1000000, 'Home maintenance'), 
-- (1, NULL, 4, 'expense', '2024-12-05', 1500000, 'New phone'), 
-- (2, NULL, 7, 'expense', '2024-12-06', 150000, 'Cash payment for groceries'), 
-- (1, NULL, 5, 'expense', '2024-12-10', 300000, 'School fees'), 
-- (1, NULL, 6, 'expense', '2024-12-15', 250000, 'Movie tickets'), 
-- (2, NULL, 2, 'expense', '2024-12-16', 50000, 'Cash payment for transportation'), 
-- (1, NULL, 7, 'expense', '2024-12-20', 500000, 'Groceries'), 
-- (1, NULL, 8, 'expense', '2024-12-25', 1000000, 'Clothes shopping'), 
-- (1, NULL, 9, 'expense', '2024-12-30', 150000, 'Phone bill'), 
-- (1, 2, NULL, 'transfer', '2024-12-31', 1000000, 'Cashed out');