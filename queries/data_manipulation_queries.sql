-- Query to view registered Customers.
SELECT id, first_name, IFNULL(last_name, 'Not on file.') AS last_name, IFNULL (uba, 'Not on file.') AS uba
FROM Customers
ORDER BY last_name, first_name;


-- Query to view Drinks in inventory.
SELECT id, name, price, stock, IF(signature = 1, "YES", "NO") AS signature
FROM Drinks
ORDER BY name;


-- Query to view cocktail recipes.
SELECT mixed_drinks.name AS mixed_drink_name, components.name AS ingredient_drink_name, ingred.quantity
FROM Ingredients as ingred
INNER JOIN Drinks AS mixed_drinks ON mixed_drinks.id = ingred.mixed_drink_id
INNER JOIN Drinks AS components ON components.id = ingred.ingredient_drink_id
ORDER BY mixed_drinks.name, ingred.quantity DESC;


-- Query to view Tabs.
SELECT Tabs.id, CONCAT_WS(" ", Customers.first_name, Customers.last_name) AS customer,
Tabs.due, IFNULL(Tabs.paid, 'Unpaid') AS paid, SUM(Drinks.price * Purchases.quantity) AS total
FROM Customers
INNER JOIN Tabs ON Tabs.customer_id = Customers.id
INNER JOIN Purchases ON Purchases.tab_id = Tabs.id
INNER JOIN Drinks ON Drinks.id = Purchases.drink_id
GROUP BY Tabs.id
ORDER BY Tabs.paid, customer;


-- Query to view Purchases.
SELECT Purchases.id, Purchases.date, CONCAT_WS(" ", Customers.first_name, Customers.last_name) AS customer,
Drinks.name AS drink, Purchases.quantity, Drinks.price * Purchases.quantity AS total
FROM Purchases
INNER JOIN Drinks ON Purchases.drink_id = Drinks.id
INNER JOIN Tabs ON Purchases.tab_id = Tabs.id
INNER JOIN Customers ON Tabs.customer_id = Customers.id
ORDER BY Purchases.date DESC, customer;


-- Query to add a new customer with colon : character being used to denote the 
-- variables that will have data from the backend programming language.
INSERT INTO Customers (first_name, last_name, uba)
VALUES (:first_name_input, :last_name_input, :uba_input);


-- Query to add a new drink with colon : character being used to denote the 
-- variables that will have data from the backend programming language.
INSERT INTO Drinks (name, price, stock, signature)
VALUES (:name_input, :price_input, :stock_input, :signature_input);


-- Query to add a new cocktail component with colon : character being used to 
-- denote the variables that will have data from the backend programming language.
INSERT INTO Ingredients (mixed_drink_id, ingredient_drink_id, quantity)
VALUES ((SELECT id FROM Drinks WHERE name = :cocktail_input), 
(SELECT id FROM Drinks WHERE name = :ingredient_input), :quantity_input);


-- Query to open a new tab with colon : character being used to denote the 
-- variables that will have data from the backend programming language.
INSERT INTO Tabs (customer_id, due, paid)
VALUES (:id_input, :due_input, :paid_input);


-- Query to record a new purchase with colon : character being used to denote 
-- the variables that will have data from the backend programming language.
INSERT INTO Purchases (tab_id, drink_id, date, quantity)
VALUES (:id_input, (SELECT Drinks.id FROM Drinks WHERE name = :drink_name_input),
    :date_input, :quantity_input);


-- Filter queries for View Customers page in the following order: First Name, 
-- Last Name, UBA Number. The colon : character is used to denote the variables 
-- that will have data from the backend programming language.
SELECT id, first_name, IFNULL(last_name, 'Not on file.') AS last_name, IFNULL (uba, 'Not on file.') AS uba
FROM Customers
WHERE first_name = :first_name_input;

SELECT id, first_name, IFNULL(last_name, 'Not on file.') AS last_name, IFNULL (uba, 'Not on file.') AS uba
FROM Customers
WHERE last_name = :last_name_input;

SELECT id, first_name, IFNULL(last_name, 'Not on file.') AS last_name, IFNULL (uba, 'Not on file.') AS uba
FROM Customers
WHERE uba = :uba_input;


-- Filter queries for View Inventory page in the following order: Drink Name, 
-- Price, Stock, Signature Cocktail. The colon : character is used to denote 
-- the variables that will have data from the backend programming language.
SELECT id, name, price, stock, IF(signature = 1, "YES", "NO") AS signature
FROM Drinks
WHERE name = :name_input;

SELECT id, name, price, stock, IF(signature = 1, "YES", "NO") AS signature
FROM Drinks
WHERE price = :price_input;

SELECT id, name, price, stock, IF(signature = 1, "YES", "NO") AS signature
FROM Drinks
WHERE stock = :stock_input;

SELECT id, name, price, stock, IF(signature = 1, "YES", "NO") AS signature
FROM Drinks
WHERE signature = :signature_input;


-- Filter queries for View Cocktails page in the following order: Cocktail, 
-- Ingredient, Quantity. The colon : character is used to denote the variables 
-- that will have data from the backend programming language.
SELECT mixed_drinks.name AS mixed_drink_name, components.name AS ingredient_drink_name, ingred.quantity
FROM Ingredients as ingred
INNER JOIN Drinks AS mixed_drinks ON mixed_drinks.id = ingred.mixed_drink_id
INNER JOIN Drinks AS components ON components.id = ingred.ingredient_drink_id
WHERE mixed_drinks.name = :cocktail_input;

SELECT mixed_drinks.name AS mixed_drink_name, components.name AS ingredient_drink_name, ingred.quantity
FROM Ingredients as ingred
INNER JOIN Drinks AS mixed_drinks ON mixed_drinks.id = ingred.mixed_drink_id
INNER JOIN Drinks AS components ON components.id = ingred.ingredient_drink_id
WHERE components.name = :ingredient_input;

SELECT mixed_drinks.name AS mixed_drink_name, components.name AS ingredient_drink_name, ingred.quantity
FROM Ingredients as ingred
INNER JOIN Drinks AS mixed_drinks ON mixed_drinks.id = ingred.mixed_drink_id
INNER JOIN Drinks AS components ON components.id = ingred.ingredient_drink_id
WHERE ingred.quantity = :quantity_input;


-- Filter queries for View Tabs page in the following order: Customer, Due, 
-- Paid, Tab Total. The colon : character is used to denote the variables that 
-- will have data from the backend programming language.
WITH compTable AS (
    SELECT Tabs.id, CONCAT_WS(" ", Customers.first_name, Customers.last_name) AS customer,
    Tabs.due, IFNULL(Tabs.paid, 'Unpaid') AS paid, SUM(Drinks.price * Purchases.quantity) AS total
    FROM Customers
    INNER JOIN Tabs ON Tabs.customer_id = Customers.id
    INNER JOIN Purchases ON Purchases.tab_id = Tabs.id
    INNER JOIN Drinks ON Drinks.id = Purchases.drink_id
    GROUP BY Tabs.id
)
SELECT id, customer, due, paid, total FROM compTable
WHERE customer = :customer_input;

WITH compTable AS (
    SELECT Tabs.id, CONCAT_WS(" ", Customers.first_name, Customers.last_name) AS customer,
    Tabs.due, IFNULL(Tabs.paid, 'Unpaid') AS paid, SUM(Drinks.price * Purchases.quantity) AS total
    FROM Customers
    INNER JOIN Tabs ON Tabs.customer_id = Customers.id
    INNER JOIN Purchases ON Purchases.tab_id = Tabs.id
    INNER JOIN Drinks ON Drinks.id = Purchases.drink_id
    GROUP BY Tabs.id
)
SELECT id, customer, due, paid, total FROM compTable
WHERE due LIKE :%due_input%;

WITH compTable AS (
    SELECT Tabs.id, CONCAT_WS(" ", Customers.first_name, Customers.last_name) AS customer,
    Tabs.due, IFNULL(Tabs.paid, 'Unpaid') AS paid, SUM(Drinks.price * Purchases.quantity) AS total
    FROM Customers
    INNER JOIN Tabs ON Tabs.customer_id = Customers.id
    INNER JOIN Purchases ON Purchases.tab_id = Tabs.id
    INNER JOIN Drinks ON Drinks.id = Purchases.drink_id
    GROUP BY Tabs.id
)
SELECT id, customer, due, paid, total FROM compTable
WHERE paid LIKE :%paid_input%;

WITH compTable AS (
    SELECT Tabs.id, CONCAT_WS(" ", Customers.first_name, Customers.last_name) AS customer,
    Tabs.due, IFNULL(Tabs.paid, 'Unpaid') AS paid, SUM(Drinks.price * Purchases.quantity) AS total
    FROM Customers
    INNER JOIN Tabs ON Tabs.customer_id = Customers.id
    INNER JOIN Purchases ON Purchases.tab_id = Tabs.id
    INNER JOIN Drinks ON Drinks.id = Purchases.drink_id
    GROUP BY Tabs.id
)
SELECT id, customer, due, paid, total FROM compTable
WHERE total = :total_input;


-- Filter queries for View Purchases page in the following order: Purchase Time, 
-- Customer, Drink, Quantity, Total; The colon : character is used to denote 
-- the variables that will have data from the backend programming language.
WITH compTable AS (
    SELECT Purchases.id, Purchases.date, CONCAT_WS(" ", Customers.first_name, Customers.last_name) AS customer,
    Drinks.name AS drink, Purchases.quantity, Drinks.price * Purchases.quantity AS total
    FROM Purchases
    INNER JOIN Drinks ON Purchases.drink_id = Drinks.id
    INNER JOIN Tabs ON Purchases.tab_id = Tabs.id
    INNER JOIN Customers ON Tabs.customer_id = Customers.id
)
SELECT id, date, customer, drink, quantity, total FROM compTable
WHERE date LIKE :%date_input%;

WITH compTable AS (
    SELECT Purchases.id, Purchases.date, CONCAT_WS(" ", Customers.first_name, Customers.last_name) AS customer,
    Drinks.name AS drink, Purchases.quantity, Drinks.price * Purchases.quantity AS total
    FROM Purchases
    INNER JOIN Drinks ON Purchases.drink_id = Drinks.id
    INNER JOIN Tabs ON Purchases.tab_id = Tabs.id
    INNER JOIN Customers ON Tabs.customer_id = Customers.id
)
SELECT id, date, customer, drink, quantity, total FROM compTable
WHERE customer = :customer_input;

WITH compTable AS (
    SELECT Purchases.id, Purchases.date, CONCAT_WS(" ", Customers.first_name, Customers.last_name) AS customer,
    Drinks.name AS drink, Purchases.quantity, Drinks.price * Purchases.quantity AS total
    FROM Purchases
    INNER JOIN Drinks ON Purchases.drink_id = Drinks.id
    INNER JOIN Tabs ON Purchases.tab_id = Tabs.id
    INNER JOIN Customers ON Tabs.customer_id = Customers.id
)
SELECT id, date, customer, drink, quantity, total FROM compTable
WHERE quantity = :quantity_input;

WITH compTable AS (
    SELECT Purchases.id, Purchases.date, CONCAT_WS(" ", Customers.first_name, Customers.last_name) AS customer,
    Drinks.name AS drink, Purchases.quantity, Drinks.price * Purchases.quantity AS total
    FROM Purchases
    INNER JOIN Drinks ON Purchases.drink_id = Drinks.id
    INNER JOIN Tabs ON Purchases.tab_id = Tabs.id
    INNER JOIN Customers ON Tabs.customer_id = Customers.id
)
SELECT id, date, customer, drink, quantity, total FROM compTable
WHERE total = :total_input;


-- Query to edit a customer's information with colon : character being used to 
-- denote the variables that will have data from the backend programming language.
UPDATE Customers
SET first_name = :first_name_input, last_name = :last_name_input, uba = :uba_input
WHERE id = :id_derived_from_edit_button;


-- Query to edit a drink's information with colon : character being used to 
-- denote the variables that will have data from the backend programming language.
UPDATE Drinks
SET name = :name_input, price = :price_input, stock = :stock_input, signature = :signature_input
WHERE id = :id_derived_from_edit_button;


-- Query to edit a cocktail's recipe with colon : character being used to denote 
-- the variables that will have data from the backend programming language.
UPDATE Ingredients
SET mixed_drink_id = (SELECT id FROM Drinks WHERE name = :cocktail_input), 
ingredient_drink_id = (SELECT id FROM Drinks WHERE name = :ingredient_input), 
quantity = :quantity_input
WHERE mixed_drink_id = (SELECT id FROM Drinks WHERE name = :cocktail_input) AND 
ingredient_drink_id = (SELECT id FROM Drinks WHERE name = :ingredient_input);


-- Query to edit a tab with colon : character being used to denote the 
-- variables that will have data from the backend programming language.
UPDATE Tabs
SET customer_id = (SELECT id FROM Customers WHERE first_name = :first_name_input AND last_name = :last_name_input),
due = :due_input, paid = :paid_input
WHERE id = :id_derived_from_edit_button;


-- Query to edit a purchase with colon : character being used to denote the 
-- variables that will have data from the backend programming language.
UPDATE Purchases
SET tab_id = :tab_input,
drink_id = (SELECT Drinks.id FROM Drinks WHERE name = :drink_name_input),
date = :date_input, quantity = :quantity_input
WHERE id = :id_derived_from_edit_button;


-- Query to delete a customer.
DELETE FROM Customers WHERE id = :id_derived_from_edit_button;


-- Query to delete a drink.
DELETE FROM Drinks WHERE id = :id_derived_from_edit_button;


-- Query to delete a cocktail ingredient.
DELETE FROM Ingredients WHERE mixed_drink_id = :id_derived_from_edit_button AND ingredient_drink_id = :id_derived_from_edit_button;


-- Query to delete a tab.
DELETE FROM Tabs WHERE id = :id_derived_from_edit_button;


-- Query to delete a purchase.
DELETE FROM Purchases WHERE id = :id_derived_from_edit_button;
