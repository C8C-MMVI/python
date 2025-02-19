# Sales list: (Product Name, Stock Quantity, Price per Unit (in PHP))
# Sales is a list variable containing tuples
sales = [
    ("Milk", 120, 55.00),
    ("Bread", 150, 40.00),
    ("Eggs", 90, 80.00),
    ("Chicken", 75, 160.00),
    ("Rice", 200, 50.00),
    ("Banana", 180, 25.00) ]

# display_sales displays the list in an organized manner
def display_sales():
    print("\nSales Record:")
    for productName, unitSales, price in sales:
        print(f"{productName}: Units sold = {unitSales}, \
Price per Unit = {price:.2f} PHP") # displays the unsorted data

# sort_sales displays a sorted list
def sort_sales():
    # uses the code sorted() to alphabetically sort the list
    sorted_sales_revenue = sorted(sales, key=lambda x: x[1] * x[2], reverse=True)
    print("\nSorted Inventory List (Based on total revenue):") # header
    for productName, unitSales, price in sorted_sales_revenue:
        print(f"{productName}: Units sold = {unitSales}, \
Price per Unit = {price:.2f} PHP") # displays the sorted data in descending order

# best_selling_product displays only the best-selling product on the
# list variable sales
def best_selling_product():
    # uses the code max() to determine the maximum
    best_selling = max(sales, key=lambda x: x[2])
    print(f"\nBest-Selling Product: {best_selling[0]} \
with a total of {best_selling[1]} units")

# total_revenue displays the total price in the inventory
def total_sales_revenue():
    revenue = sum(unitSales * price for _, unitSales, price in sales)
    print(f"\nTotal Sales Revenue: {revenue:.2f} PHP")

# add_new_sales lets the user declare new data and
# displays the updated list
def add_new_sales():
    print("\nAdd a new sales entry") # header
    product_name = input("Enter a new product name: ") 
    units_sold = int(input("Enter the units sold: "))
    price = float(input("Enter the price per unit: "))
    sales.append((product_name, units_sold, price)) # adds the user's input
    print("\nUpdated Inventory List:")
    display_sales() # updated list var sales and puts the user input at last

# main displays the methods
def main():
    display_sales()
    sort_sales()
    best_selling_product()
    total_sales_revenue()
    add_new_sales()

if __name__ == "__main__":
    main()



