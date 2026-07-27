# Customer
- Id (Primary key)
- Name
- DoB
- Street_Address
- City
- State
- Zip Codea

# Credit_Card
- Credit_Card_Number (Primary Key)
- Name
- CVC
- Street_Address
- City
- State
- Zip Code

# Credit_Card_Customer
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

# Inventory_Updates
- (Staff_Id, Product_Id, Date_Updated) (Primary key)
- Date_Updated
- Staff_Id (References Id in Staff)
- Product_Id (References Id in Product)
- Old_Price
- New_Price
- Quantity_Change
- New_Quantity
- Active

# Rate
- (Customer_Id, Product_Id) (Primary key)
- Customer_Id (References Id in Customer)
- Product_Id (References Id in Product)
- Rating
- Description

# Purchase
- Id (Primary key)
- Customer_Id (References Id in Customer)
- Card_Number (References Credit_Card_Number in Credit_Card)
- Total Price
- Purchase_Date

# Purchased_Items
- (Purchase_Id, Product_Id) (Primary key)
- Purchase_Id (References Id in Purchase)
- Product_Id (References Id in Product)
- Unit_Price
- Quantity