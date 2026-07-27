-- When declaring a primary key it has to be INTEGER and not INT to auto-increment

DROP TABLE IF EXISTS Staff;

DROP TABLE IF EXISTS Product;

CREATE TABLE IF NOT EXISTS Staff (
    Id INTEGER PRIMARY KEY NOT NULL,
    Name NVARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Product (
    Id INTEGER PRIMARY KEY NOT NULL,
    Name NVARCHAR(50) NOT NULL UNIQUE,
    -- SQLite doesn't have a money type so you'll have to divide by 100 to get the actual value
    Price INT NOT NULL,
    Quantity INT NOT NULL,
    Active BOOLEAN NOT NULL
);

-- Seeding database
INSERT INTO
    Staff (Name)
VALUES
    ('Brian'),
    ('Morgan');

INSERT INTO
    Product (Name, Price, Quantity, Active)
VALUES
    ("Orange", 500, 10, 1),
    ("TV", 50000, 3, 1),
    ("Owala Bottle", 3000, 57, 1);