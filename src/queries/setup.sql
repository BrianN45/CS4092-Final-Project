-- When declaring a primary key it has to be INTEGER and not INT to auto-increment

DROP TABLE IF EXISTS Inventory_Updates;

DROP TABLE IF EXISTS Staff;

DROP TABLE IF EXISTS Product;

DROP TABLE IF EXISTS CreditCard;

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

CREATE TABLE IF NOT EXISTS Inventory_Updates (
    Staff_Id INT NOT NULL,
    Product_Id INT NOT NULL,
    Date_Updated DATE NOT NULL DEFAULT CURRENT_DATE,
    Old_Price INT NOT NULL,
    New_Price INT NOT NULL,
    Quantity_Change INT NOT NULL,
    New_Quantity INT NOT NULL,
    Active BOOLEAN NOT NULL,
    PRIMARY KEY (Staff_Id, Product_Id, Date_Updated),
    FOREIGN KEY (Staff_Id) REFERENCES Staff(Id),
    FOREIGN KEY (Product_Id) REFERENCES Product(Id)
);

CREATE TABLE IF NOT EXISTS Credit_Card (
    CardNumber NVARCHAR(16) PRIMARY KEY NOT NULL UNIQUE,
    Name NVARCHAR(50) NOT NULL,
    CVC NVARCHAR(3) NOT NULL,
    ExpirationDate NVARCHAR(5) NOT NULL,
    StreetAddress NVARCHAR(100) NOT NULL,
    City NVARCHAR(50) NOT NULL,
    State NVARCHAR(2) NOT NULL,
    ZipCode NVARCHAR(10) NOT NULL
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

INSERT INTO
    CreditCard (CardNumber, Name, CVC, ExpirationDate, StreetAddress, City, State, ZipCode)
VALUES
    ("1234567890123456", "John Doe", "123", "12/25", "123 Main St", "Anytown", "ST", "12345");
