-- Drop any existing tables that will conflict with new tables.
DROP TABLE IF EXISTS `Purchases`;
DROP TABLE IF EXISTS `Ingredients`;
DROP TABLE IF EXISTS `Tabs`;
DROP TABLE IF EXISTS `Drinks`;
DROP TABLE IF EXISTS `Customers`;


-- Create Customers table
CREATE TABLE Customers (
    id int AUTO_INCREMENT NOT NULL,
    first_name varchar(255) NOT NULL,
    last_name varchar(255),
    uba char(20) UNIQUE,
    PRIMARY KEY (id)
) ENGINE=INNODB;


-- Create Drinks table
CREATE TABLE Drinks (
    id int AUTO_INCREMENT NOT NULL,
    name varchar(255) UNIQUE NOT NULL,
    price decimal(7,2) NOT NULL,
    stock decimal(7,2) NOT NULL,
    signature boolean NOT NULL DEFAULT 0,
    PRIMARY KEY(id)
) ENGINE=INNODB;


-- Create Tabs table
CREATE TABLE Tabs (
    id int AUTO_INCREMENT NOT NULL,
    customer_id int NOT NULL,
    due timestamp NOT NULL,
    paid timestamp NULL DEFAULT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY fk_customer(customer_id)
    REFERENCES Customers(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) ENGINE=INNODB;


-- Create Purchases table
CREATE TABLE Purchases (
    id int AUTO_INCREMENT NOT NULL,
    tab_id int NOT NULL,
    drink_id int NOT NULL,
    date timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    quantity int NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY fk_tab(tab_id)
    REFERENCES Tabs(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    FOREIGN KEY fk_drink(drink_id)
    REFERENCES Drinks(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) ENGINE=INNODB;


-- Create Ingredients table
CREATE TABLE Ingredients (
    mixed_drink_id int NOT NULL,
    ingredient_drink_id int NOT NULL,
    quantity decimal(4,2) NOT NULL,
    PRIMARY KEY(mixed_drink_id, ingredient_drink_id),
    FOREIGN KEY fk_mixed_drink(mixed_drink_id)
    REFERENCES Drinks(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    FOREIGN KEY fk_ingredient(ingredient_drink_id)
    REFERENCES Drinks(id)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) ENGINE=INNODB;


-- Populate the Customers table
INSERT INTO Customers (id, first_name, last_name, uba)
VALUES
    (1, 'Tom', 'Bombadil', 'C3A74628F5DB39ABBD2D'),
    (2, 'Zaphod', 'Beeblebrox', '69F2A929547FCEFD846E'),
    (3, 'Bender', 'Rodriguez', 'C3B23141C09259CA37A5'),
    (4, 'Turanga', 'Leela', '2EAF8CB70C4B6676AF47'),
    (5, 'Han', 'Solo', '9A458062E04CCC48BBF6'),
    (6, 'Ellen', 'Ripley', '47CB09C9E9350A65B804'),
    (7, 'James', 'Kirk', NULL),
    (8, 'Rod', 'Serling', 'B9FED8679B355C07FBF3'),
    (9, 'Nyota', 'Uhura', '76EF076839F7C64685CB'),
    (10, 'Quark', NULL, 'FE553D8EFF7AA2E83274'),
    (11, 'Norrin', 'Radd', '8B57283C06A91195EA39'),
    (12, 'Kal', 'El', NULL);


-- Populate the Drinks table
INSERT INTO Drinks (id, name, price, stock, signature)
VALUES
    (1, 'Gin (House)', 8, 9600, 0),
    (2, 'Gin (Top Shelf)', 12, 2240, 0),
    (3, 'Rum (House)', 8, 7040, 0),
    (4, 'Rum (Top Shelf)', 12, 2560, 0),
    (5, 'Tequila (House)', 8, 10240, 0),
    (6, 'Tequila (Top Shelf)', 12, 2880, 0),
    (7, 'Vodka (House)', 8, 7680, 0),
    (8, 'Vodka (Top Shelf)', 12, 1920, 0),
    (9, 'Bourbon (House)', 8, 8960, 0),
    (10, 'Bourbon (Top Shelf)', 14, 2880, 0),
    (11, 'Scotch (House)', 8, 7680, 0),
    (12, 'Scotch (Top Shelf)', 14, 2240, 0),
    (13, 'Cointreau', 10, 6320, 0),
    (14, 'Lime Juice', 1, 5360, 0),
    (15, 'Sweet Vermouth', 10, 1760, 0),
    (16, 'Cabernet Sauvignon', 8, 2300, 0),
    (17, 'Pinot Noir', 9, 1985, 0),
    (18, 'Chardonnay', 7, 2425, 0),
    (19, 'Pinot Grigio', 9, 2020, 0),
    (20, 'Rosé', 9, 1860, 0),
    (21, 'Champagne', 14, 3010, 0),
    (22, 'Beer Brand Beer', 3, 4608, 0),
    (23, 'Red Stripe', 5, 2688, 0),
    (24, 'Hubble Home Brew', 8, 1152, 0),
    (25, "Asimov's Margarita", 15, 0, 1),
    (26, 'Quagfire Tarball', 14, 0, 1),
    (27, 'Venuthian Rosé', 16, 0, 1),
    (28, "Cosmo's Cosmopolitan", 18, 0, 1),
    (29, 'Alderaan Iced Tea', 16, 0, 1);


-- Populate the Ingredients table
INSERT INTO Ingredients (mixed_drink_id, ingredient_drink_id, quantity)
VALUES
    (25, 5, 4),
    (25, 13, 2.67),
    (25, 14, 1.33),
    (26, 9, 1.67),
    (26, 15, 0.67),
    (27, 1, 1),
    (27, 14, 0.5),
    (27, 20, 2),
    (28, 7, 1.33),
    (28, 13, 0.33),
    (28, 14, 0.33),
    (29, 7, 0.5),
    (29, 3, 0.5),
    (29, 5, 0.5),
    (29, 1, 0.5),
    (29, 13, 0.5);


-- Populate the Tabs table
INSERT INTO Tabs (id, customer_id, due, paid)
VALUES
    (1, 2, '2020-03-12 19:23:02', '2020-02-10 20:15:32'),
    (2, 6, '2020-03-16 23:31:18', '2020-02-15 00:12:08'),
    (3, 9, '2020-03-20 21:15:42', '2020-02-18 21:40:33'),
    (4, 7, '2020-03-20 21:33:41', '2020-02-18 21:40:33'),
    (5, 5, '2020-03-22 13:15:07', NULL),
    (6, 3, '2020-03-23 10:01:30', NULL);


-- Populate the Purchases table
INSERT INTO Purchases (id, tab_id, drink_id, date, quantity)
VALUES
    (1, 1, 5, '2020-02-10 19:23:02', 4),
    (2, 1, 23, '2020-02-10 19:23:02', 4),
    (3, 1, 26, '2020-02-10 20:04:47', 2),
    (4, 1, 27, '2020-02-10 20:04:47', 2),
    (5, 2, 10, '2020-02-14 23:31:18', 1),
    (6, 2, 10, '2020-02-15 00:10:03', 1),
    (7, 3, 18, '2020-02-18 21:15:42', 1),
    (8, 4, 18, '2020-02-18 21:33:41', 1),
    (9, 4, 12, '2020-02-18 21:33:41', 1),
    (10, 4, 18, '2020-02-18 21:37:20', 1),
    (11, 4, 12, '2020-02-18 21:37:20', 1),
    (12, 5, 22, '2020-02-20 13:15:07', 1),
    (13, 5, 22, '2020-02-20 13:34:22', 1),
    (14, 5, 22, '2020-02-20 13:49:53', 1),
    (15, 6, 22, '2020-02-21 10:01:30', 3),
    (16, 6, 22, '2020-02-21 10:05:21', 3),
    (17, 6, 22, '2020-02-21 10:10:21', 3);
