# Customer
- Id (Primary key)
- Name
- DoB
- Street_Address
- City
- State
- Zip Code

# CreditCard
- Credit_Card_Number (Primary Key)
- Name
- CVC
- Expiry_Date
- Street_Address
- City
- State
- Zip Code

# CreditCardCustomer
- (Credit_Card_Number, Customer_Id) (Primary key)
- Credit_Card_Number (References Credit_Card_Number in Credit_Card)
- Customer_Id (References Id in Customer)

# Product
- Id (Primary key)
- Quantity
- Active
- Price
- Name

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

# Purchase
- Id (Primary key)
- Customer_Id (References Id in Customer)
- Card_Number (References Credit_Card_Number in Credit_Card)
- Total Price
- Purchase_Date

# PurchasedItems
- (Purchase_Id, Product_Id) (Primary key)
- Purchase_Id (References Id in Purchase)
- Product_Id (References Id in Product)
- Unit_Price
- Quantity