from datetime import date
import sqlite3
connection = sqlite3.connect(
    r"C:\Users\brand\Desktop\CS\Personal\Cemex\Database\meal_orders.db..db"
)
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

order_date = date.today().isoformat()
cursor.execute(
    """INSERT INTO orders (employee_id, order_date, order_cost)
    VALUES (?, ?, ?)""",
    (employee_id, order_date, order_cost))
connection.commit()
order_id = cursor.lastrowid
print("Order created! Order ID:", order_id)

for meal_id, meal_name, quantity, item_cost in valid_items:
    cursor.execute(
        """INSERT INTO order_items (order_id, meal_id, quantity, price_at_order)
        VALUES (?, ?, ?, ?)""",
     (order_id, meal_id, quantity, item_cost)
    )
connection.commit()
connection.close()
print("Order items inserted successfully.")