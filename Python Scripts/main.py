#Imported date time formats and sqlite3 to allow for the creation of a database and the insertion of data into it
from datetime import date
import sqlite3
connection = sqlite3.connect(r"C:\Users\brand\Desktop\CS\Personal\Cemex\Food Ordering\Database\meal_orders.db..db"
)
cursor= connection.cursor()

#BUILDING THE ORDERING LOGIC

#Allow for checks of empoyee ID's. Invalid ID's will end the programme
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

#Set variables to calculate costs and set list of tuples to allow for multiple meals
order_cost = 0
valid_items = []
meal_selection = [(99,1),(3,4),(7,3)]
#For loops to allow for meal selection and ignore invalid meals but continue running instead of closing the script
for meal_id, quantity in meal_selection:
    cursor.execute(
    "SELECT * FROM meals WHERE meal_id = ?", (meal_id,))
    meals = cursor.fetchone()
    print (meals)

    if meals is None:
        print(f"Meal {meal_id} not found.")
        continue
    
    elif meals[3]== 0:
        print(f"Meal {meals[1]} not  available.")
        continue

    else:
        print("Meal is available.")

    item_cost = meals[2]
    meal_cost = item_cost * quantity
    order_cost += meal_cost
    valid_items.append((meal_id, meals[1], quantity, item_cost))
print("Order total:", order_cost)
print(valid_items)

#This injects the entire order into the database's Order table as 1 unit
order_date = date.today().isoformat()
cursor.execute(
    """INSERT INTO orders (employee_id, order_date, order_cost)
    VALUES (?, ?, ?)""",
    (employee_id, order_date, order_cost))
connection.commit()
order_id = cursor.lastrowid
print("Order created! Order ID:", order_id)

#This injects each individual order from the main order into the Order_Items table
for meal_id, meal_name, quantity, item_cost in valid_items:
    cursor.execute(
        """INSERT INTO order_items (order_id, meal_id, quantity, price_at_order)
        VALUES (?, ?, ?, ?)""",
     (order_id, meal_id, quantity, item_cost)
    )
connection.commit()
connection.close()
print("Order items inserted successfully.")


#Adjustments made are as follows:
#The script still does not tolerate invalid employee ID'S
#The script ignores invalid meals instead of stopping and also improves the assignment of orders to the database tables
#The script calculates the total cost of the order and ordr items and inserts it into the rigth tables