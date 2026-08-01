# Customer
- Id (Primary key)
- Name
- DoB
- StreetAddress
- City
- State
- ZipCode

# CreditCard
- CardNumber (Primary Key)
- Name
- CVC
- ExpirationDate
- StreetAddress
- City
- State
- ZipCode

# CreditCardCustomer
- (CustomerId, CardNumber) (Primary key)
- CustomerId (References Id in Customer)
- CardNumber (References CardNumber in CreditCard)

# Product
- Id (Primary key)
- Name
- Price
- Quantity
- Active

# Staff
- Id (Primary key)
- Name

# InventoryUpdates
- (Staff_Id, Product_Id, Date_Updated) (Primary key)
- Date_Updated
- Staff_Id (References Id in Staff)
- Product_Id (References Id in Product)
- Old_Price
- New_Price
- Quantity_Change
- New_Quantity
- Active

# Rating
- (Customer_Id, Product_Id) (Primary key)
- Customer_Id (References Id in Customer)
- Product_Id (References Id in Product)
- Rate
- Description

# Cart
- (CustomerId, ProductId) (Primary key)
- CustomerId (References Id in Customer)
- ProductId (References Id in Product)
- Quantity

# Purchase
- Id (Primary key)
- CustomerId (References Id in Customer)
- CardNumber (References CardNumber in CreditCard)
- TotalPrice
- PurchaseDate

# PurchasedItem
- (PurchaseId, ProductId) (Primary key)
- PurchaseId (References Id in Purchase)
- ProductId (References Id in Product)
- UnitPrice
- Quantity