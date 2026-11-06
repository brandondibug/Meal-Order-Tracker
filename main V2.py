#V2:
# This script is a continuation of the meal ordering script. It will allow for multiple meals
#  to be ordered at once, and will also stop the script if an invalid employee ID or meal ID is given.


#CONNECTING TO THE DATABASE

from datetime import date
import sqlite3
connection = sqlite3.connect(
    r"C:\Users\brand\Desktop\CS\Personal\Cemex\Database\meal_orders.db..db"
)
# The full file path was used above to ensure the databse would link
cursor= connection.cursor()

#BUILDING THE ORDERING LOGIC

employee_id = 1000
cursor.execute(
    "SELECT * FROM employees WHERE employee_id = ?", (employee_id,))
employee= cursor.fetchone()
if employee is None:
    print("Employee not found.")
    connection.close()
    raise SystemExit
else:
    print (employee)

order_cost = 0
valid_items = []
meal_selection = [(2,1),(3,4),(7,3)]
for meal_id, quantity in meal_selection:
    cursor.execute(
    "SELECT * FROM meals WHERE meal_id = ?", (meal_id,))
    meals = cursor.fetchone()
    print (meals)

    if meals is None:
        print("Meal not found.")
        connection.close()
        raise SystemExit
    
    elif meals[3]== 0:
        print("Meal is not available.")
    else:
        print("Meal is available.")

    item_cost = meals[2]
    meal_cost = item_cost * quantity
    order_cost += meal_cost
    valid_items.append((meal_id, quantity, item_cost))
print("Order total:", order_cost)

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
    (order_id, meal_id, quantity, meals[2])
)
connection.commit()



#Adjustments made are as follows:
#The script accepts multiple meal orders
#The script will stop if an invalid employee ID or meal ID is given
#The script calculates the total cost of the order and inserts it into the orders table


#V3 will allow the script to ignore invalid meals and also improve the assignmetn of orders to the database