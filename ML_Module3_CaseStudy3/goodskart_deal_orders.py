import csv
import re


# Custom Exception

class CustomerNotAllowedException(Exception):
    """Raised when customer is blacklisted."""
    pass



# Customer Class

class Customer:
    def __init__(self, title, first_name, last_name, email, phone, blacklisted):
        self.title = title
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.blacklisted = int(blacklisted)

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name} ({self.email})"



# Order Class

class Order:
    def __init__(self, customer, product_name, product_code):
        self.customer = customer
        self.product_name = product_name
        self.product_code = product_code

    def __str__(self):
        return (f"Order for {self.customer.first_name} {self.customer.last_name} "
                f"- Product: {self.product_name} (Code: {self.product_code})")



# Function to create order
def createOrder(customer, product_name, product_code):
    if customer.blacklisted == 1:
        raise CustomerNotAllowedException(
            f"Customer {customer.first_name} {customer.last_name} is blacklisted!"
        )
    return Order(customer, product_name, product_code)


# -------------------------------
def parse_customer_name(full_name):
    """
    Splits title, first name, and last name using regex.
    Example: 'Mr. John Smith' -> ('Mr.', 'John', 'Smith')
    """
    match = re.match(r'(\w+\.)\s+(\w+)\s+(\w+)', full_name)
    if match:
        return match.groups()
    else:
        return ("", "", "")
# -------------------------------
customers = []

# Read CSV (FairDealCustomerData.csv)
with open('FairDealCustomerData.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        title, first_name, last_name = parse_customer_name(row['Name'])
        customer = Customer(
            title,
            first_name,
            last_name,
            row['Email'],
            row['Phone'],
            row['Blacklisted']
        )
        customers.append(customer)

print(f"Loaded {len(customers)} customers from FairDeal data.")

# Simulate order creation
while True:
    choice = input("\nEnter customer email to place order (or type 'END' to quit): ").strip()
    if choice.upper() == "END":
        print("Exiting system. Goodbye!")
        break

    # Find customer by email
    selected_customer = next((c for c in customers if c.email.lower() == choice.lower()), None)

    if not selected_customer:
        print(" Customer not found.")
        continue

    product_name = input("Enter product name: ").strip()
    product_code = input("Enter product code: ").strip()

    try:
        order = createOrder(selected_customer, product_name, product_code)
        print(f" Order Created Successfully!\n{order}")
    except CustomerNotAllowedException as e:
        print(f" {e}")

# End of recent edits
print("Thank you for using the Goodskart Deal Orders System.")      

