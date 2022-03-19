queries = {
    'read_customers':'''
SELECT id AS id, first_name, IFNULL(last_name, 'Not on file') AS
last_name, IFNULL(uba, 'Not on file') AS uba FROM Customers''',
    'read_drinks':'''
SELECT id, name, price, stock, IF(signature, 'Yes', 'No') AS
signature FROM Drinks''',
    'read_ingredients':'''
SELECT ing_d.id AS ingredient_drink_id, mix_d.id AS mixed_drink_id, mix_d.name AS mixed_drink_name,
ing_d.name AS ingredient_drink_name, i.quantity
FROM Ingredients AS i
INNER JOIN Drinks AS mix_d ON mix_d.id = i.mixed_drink_id
INNER JOIN Drinks AS ing_d ON ing_d.id = i.ingredient_drink_id''',
    'read_ingredients_for':'''
SELECT ing_d.id AS ingredient_drink_id, mix_d.id AS mixed_drink_id, ing_d.name, i.quantity 
FROM Drinks AS mix_d
INNER JOIN Ingredients AS i ON mix_d.id = i.mixed_drink_id
INNER JOIN Drinks AS ing_d ON ing_d.id = i.ingredient_drink_id
WHERE mix_d.id = {0}''',
    'read_purchases':'''
SELECT p.id AS id, p.date AS date, 
CONCAT_WS(' ',
CONCAT_WS(' ', c.first_name, c.last_name),
CONCAT(' (#', c.id, ')')) AS customer, 
d.name AS drink, p.quantity AS quantity, d.price * p.quantity AS total
FROM Purchases AS p
INNER JOIN Drinks AS d ON p.drink_id = d.id
INNER JOIN Tabs AS t ON p.tab_id = t.id
INNER JOIN Customers AS c ON t.customer_id = c.id 
ORDER BY p.date DESC''',
    'read_tabs':'''
SELECT t.id, 
CONCAT(CONCAT_WS(" ", c.first_name, c.last_name), ' (#', c.id, ')') AS customer, 
t.due AS due,
IFNULL(t.paid, 'Unpaid') AS paid,
SUM(d.price * p.quantity) AS total
FROM Tabs AS t
INNER JOIN Customers AS c ON t.customer_id = c.id
LEFT JOIN
(Purchases AS p INNER JOIN Drinks AS d ON d.id = p.drink_id)
ON p.tab_id = t.id
GROUP BY t.id''',
    'customers_form':'''
SELECT * FROM Customers''',
    'drinks_form':'''
SELECT * FROM Drinks''',
    'ingredients_form':'''
SELECT * FROM Ingredients''',
    'purchases_form':'''
SELECT * FROM Purchases''',
    'tabs_form':'''
SELECT * FROM Tabs''',
    'edit_ingredients_form':'''
SELECT mix_d.name AS mixed_drink_id, 
ing_d.name AS ingredient_drink_id, 
i.quantity
FROM Ingredients AS i
INNER JOIN Drinks AS mix_d ON mix_d.id = i.mixed_drink_id
INNER JOIN Drinks AS ing_d ON ing_d.id = i.ingredient_drink_id
WHERE mix_d.id = {0} AND ing_d.id = {1} LIMIT 1''',
    'tab_id_dropdown':'''
SELECT t.id,
CONCAT_WS(" for ", CONCAT('Tab #', t.id),
CONCAT(CONCAT_WS(" ", c.first_name, c.last_name), 
CONCAT(' (Customer #', c.id, ')'))) AS customer
FROM Tabs AS t
INNER JOIN Customers AS c ON t.customer_id = c.id
WHERE t.paid IS NULL
GROUP BY t.id''',
    'drink_id_dropdown':'''
SELECT id, name FROM Drinks ORDER BY name''',
    'ingredient_drink_id_dropdown':'''
SELECT id, name FROM Drinks ORDER BY name''',
    'mixed_drink_id_dropdown':'''
SELECT id, name FROM Drinks ORDER BY name''',
    'customer_id_dropdown':'''
SELECT id, 
CONCAT(CONCAT_WS(" ", c.first_name, c.last_name), ' (#', c.id, ')') AS customer
FROM Customers AS c
ORDER BY first_name, last_name''',
    'create': '''
INSERT INTO {0}{1} VALUES {2}''',
    'update': '''
UPDATE {0} SET {1} WHERE {2}'''
}
