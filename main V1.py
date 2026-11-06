#CONNECTING TO THE DATABASE

from datetime import date
import sqlite3
connection = sqlite3.connect(
    r"C:\Users\brand\Desktop\CS\Personal\Cemex\Database\meal_orders.db..db"
)
# The full file path was used above to ensure the databse would link
cursor= connection.cursor()

#Test scripts to pull all employees and meals
cursor.execute("SELECT * FROM employees;")
employees= cursor.fetchall()
print(employees)
cursor.execute("SELECT * FROM meals;")
meals= cursor.fetchall()
print(meals)

#BUILDING THE ORDERING LOGIC

# First, we will allow our script to find an employee
employee_id = 10373
cursor.execute(
    "SELECT * FROM employees WHERE employee_id = ?", (employee_id,))
employee= cursor.fetchone()
if employee is None:
    print("Employee not found.")
else:
    print (employee)

# Next, let's see if we can find a meal
meal_id = 2
cursor.execute(
    "SELECT * FROM meals WHERE meal_id = ?", (meal_id,))
meal = cursor.fetchone()
print (meal)

# Meal Validity
if meal is None:
    print("Meal not found.")
elif meal[3]== 0:
    print("Meal is not available.")
else:
    print("Meal is available.")

# Pulling the cost of the meal from the table and calculating the total cost
meal_cost = meal[2]
print("Meal cost:", meal_cost)
quantity = 1
order_cost = meal_cost * quantity
print("Quantity:", quantity)
print("Order total:", order_cost)

# Creating order dates and order ID's and inserting the order into the database
# Creating the database already had the order_id as an auto incrementing primary key,
# so we don't need to worry about that
order_date = date.today().isoformat()
cursor.execute(
    """INSERT INTO orders (employee_id, order_date, order_cost)
    VALUES (?, ?, ?)""",
    (employee_id, order_date, order_cost))
connection.commit()
order_id = cursor.lastrowid
print("Order created! Order ID:", order_id)
cursor.execute(
    """INSERT INTO order_items (order_id, meal_id, quantity, price_at_order)
    VALUES (?, ?, ?, ?)""",
    (order_id, meal_id, quantity, meal[2])
)
connection.commit()


# The limitation of this script is that it only allows for one meal to be ordered at a time.
# Also, the script continues to run even if the employee ID or meal ID given is incorrect. 
# These will be corrected in V2.