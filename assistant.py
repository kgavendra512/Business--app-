pin = input("PIN डालो: ")

if pin != "1234":
    print("Wrong PIN!")
    exit()

print("Login successful!")

import sqlite3
from datetime import date
import shutil


# ================= DATABASE =================

db = sqlite3.connect("business.db")
cursor = db.cursor()

# Sales table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    customer TEXT,
    product TEXT,
    amount INTEGER,
    date TEXT
)
""")

# Expenses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY,
    reason TEXT,
    amount INTEGER,
    date TEXT
)
""")

db.commit()

def customer_history():
    customer = input("Customer name: ")

    cursor.execute(
        """
        SELECT date, product, quantity, amount
        FROM sales
        WHERE LOWER(customer) = LOWER(?)
        ORDER BY id
        """,
        (customer,)
    )

    purchases = cursor.fetchall()

    print("===== Customer History =====")

    if not purchases:
        print("Customer nahi mila.")
        return

    total = 0

    for date_value, product, quantity, amount in purchases:
        print(
            "Date:", date_value,
            "| Product:", product,
            "| Qty:", quantity,
            "| Amount: ₹" + str(amount)
        )
        total += amount

    print("----------------------------")
    print("Total Purchase: ₹", total)

def quick_sale():
    customer = input("Customer name: ")
    product = input("Product name: ")

    cursor.execute(
        "SELECT quantity, price FROM stock WHERE product = ?",
        (product,)
    )

    item = cursor.fetchone()

    if item is None:
        print("Product stock me nahi hai.")
        return

    stock_quantity, price = item

    print("Available stock:", stock_quantity)
    print("Selling price: ₹", price)

    quantity = int(input("Kitni quantity bechi? "))

    if quantity <= 0:
        print("Quantity 0 se zyada honi chahiye.")
        return

    if quantity > stock_quantity:
        print("Itna stock available nahi hai.")
        return

    total = quantity * price
    today = str(date.today())

    cursor.execute(
        "INSERT INTO sales (customer, product, amount, date, quantity) VALUES (?, ?, ?, ?, ?)",
        (customer, product, total, today, quantity)
    )

    cursor.execute(
        "UPDATE stock SET quantity = quantity - ? WHERE product = ?",
        (quantity, product)
    )

    db.commit()

    print("Sale successfully save ho gayi!")
    print("Customer:", customer)
    print("Total: ₹", total)

# ================= ADD SALE =================


def add_sale():
    customer = input("Customer name: ")
    product = input("Product name: ")

    cursor.execute(
        "SELECT quantity FROM stock WHERE product = ?",
        (product,)
    )

    stock = cursor.fetchone()

    if stock is None:
        print("Product stock me nahi hai.")
        return

    print("Available stock:", stock[0])

    while True:
        quantity = input("Kitni quantity bechi? ")

        try:
            quantity = int(quantity)

            if quantity <= 0:
                print("Quantity 0 se zyada honi chahiye.")
                continue

            if quantity > stock[0]:
                print("Itna stock available nahi hai.")
                continue

            break

        except ValueError:
            print("Number likho. Example: 2")

    while True:
        sale = input("Sale amount: ₹")

        try:
            sale = int(sale)

            if sale < 0:
                print("Amount 0 se kam nahi hona chahiye.")
                continue
            break

        except ValueError:
            print("Number likho. Example: 5")

    today = str(date.today())

    cursor.execute(
        "INSERT INTO sales (customer, product, amount, date, quantity) VALUES (?, ?, ?, ?, ?)",
    (customer, product, sale, today, quantity)
)


    db.commit()

    cursor.execute(
        "UPDATE stock SET quantity = quantity - ? WHERE product = ?",
        (quantity, product)
    )

    db.commit()

    print("Sale database me save ho gayi!")


# ================= ADD EXPENSE =================

def add_expense():
    reason = input("Expense kis liye hua? ")

    while True:
        expense = input("Expense amount: ₹")

        try:
            expense = int(expense)

            if expense < 0:
                print("Amount 0 se kam nahi hona chahiye.")
                continue

            break

        except ValueError:
            print("Number likho. Example: 300")

    today = str(date.today())

    cursor.execute(
        """
        INSERT INTO expenses (reason, amount, date)
        VALUES (?, ?, ?)
        """,
        (reason, expense, today)
    )

    db.commit()

    print("Expense database me save ho gaya!")


# ================= TODAY SALES =================

def today_total():
    today = str(date.today())

    cursor.execute(
        "SELECT SUM(amount) FROM sales WHERE date = ?",
        (today,)
    )

    total = cursor.fetchone()[0] or 0

    print("Aaj ki Total Sales: ₹", total)


# ================= TODAY EXPENSE =================

def today_expense():
    today = str(date.today())

    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE date = ?",
        (today,)
    )

    total = cursor.fetchone()[0] or 0

    print("Aaj ka Total Expense: ₹", total)


# ================= TODAY PROFIT =================

def today_profit():
    today = str(date.today())

    cursor.execute(
        "SELECT SUM(amount) FROM sales WHERE date = ?",
        (today,)
    )

    sales = cursor.fetchone()[0] or 0

    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE date = ?",
        (today,)
    )

    expenses = cursor.fetchone()[0] or 0

    profit = sales - expenses

    print("Aaj ki Sales: ₹", sales)
    print("Aaj ka Expense: ₹", expenses)
    print("Aaj ka Profit: ₹", profit)


# ================= SALES HISTORY =================

def sales_history():
    cursor.execute(
        """
        SELECT id, date, customer, product, amount, quantity
        FROM sales
        ORDER BY id
        """
    )

    sales = cursor.fetchall()

    print("===== Sales History =====")
    print()
    print(f"{'ID':4} {'Date':10} {'Customer':10} {'Product':10} {'Qty':5} Amount")

    total = 0

    for sale in sales:
        sale_id, date_value, customer, product, amount, quantity = sale

        if amount is None:
            continue

        if quantity is None:
            quantity = "N/A"

        print(
            f"{sale_id:<4} "
            f"{str(date_value):10} "
            f"{customer:10} "
            f"{product:10} "
            f"{str(quantity):5} "
            f"₹{amount}"
        )

        total += amount

    print("-----------------------------------------")
    print("Total Sales: ₹", total)

def sale_details():
    sale_id = input("Sale ID: ")

    cursor.execute(
        "SELECT id, date, customer, product, amount, quantity FROM sales WHERE id = ?",
        (sale_id,)
    )

    sale = cursor.fetchone()

    if sale is None:
        print("Sale nahi mili.")
        return

    sale_id, date_value, customer, product, amount, quantity = sale

    if quantity is None:
        quantity = "N/A"

    print("===== Sale Details =====")
    print("ID:", sale_id)
    print("Date:", date_value)
    print("Customer:", customer)
    print("Product:", product)
    print("Quantity:", quantity)
    print("Amount: ₹", amount)


def edit_sale():
    sale_id = input("Sale ID: ")

    cursor.execute(
        "SELECT id, customer, amount FROM sales WHERE id = ?",
        (sale_id,)
    )

    sale = cursor.fetchone()

    if sale is None:
        print("Sale nahi mili.")
        return

    print("Current Customer:", sale[1])
    print("Current Amount: ₹", sale[2])

    customer = input("New customer name: ")

    while True:
        try:
            amount = int(input("New amount: ₹"))

            if amount < 0:
                print("Amount 0 se kam nahi ho sakta.")
                continue

            break

        except ValueError:
            print("Number likho. Example: 500")

    cursor.execute(
        "UPDATE sales SET customer = ?, amount = ? WHERE id = ?",
        (customer, amount, sale_id)
    )

    db.commit()

    print("Sale successfully update ho gayi!")

def delete_sale():
    sale_id = input("Sale ID: ")

    cursor.execute(
        "SELECT product, quantity, customer, amount FROM sales WHERE id = ?",
        (sale_id,)
    )

    sale = cursor.fetchone()

    if sale is None:
        print("Sale nahi mili.")
        return

    product, quantity, customer, amount = sale

    print("Customer:", customer)
    print("Product:", product)
    print("Quantity:", quantity)
    print("Amount: ₹", amount)

    confirm = input("Delete karna hai? (yes/no): ")

    if confirm.lower() != "yes":
        print("Delete cancel ho gaya.")
        return

    if quantity is not None:
        cursor.execute(
            "UPDATE stock SET quantity = quantity + ? WHERE product = ?",
            (quantity, product)
        )

    cursor.execute(
        "DELETE FROM sales WHERE id = ?",
        (sale_id,)
    )

    db.commit()

    print("Sale delete ho gayi aur stock restore ho gaya!")

# ================= EXPENSE HISTORY =================

def expense_history():
    cursor.execute(
        """
        SELECT date, reason, amount
        FROM expenses
        ORDER BY id
        """
    )

    expenses = cursor.fetchall()

    print("===== Expense History =====")

    total = 0

    for expense in expenses:
        date_value, reason, amount = expense

        print(
            "Date:", date_value,
            "| Reason:", reason,
            "| Expense: ₹" + str(amount)
        )

        total += amount

    print("Total Expense: ₹", total)


# ================= CUSTOMER TOTAL =================

def customer_total():
    customer = input("Customer name: ")

    cursor.execute(
        """
        SELECT SUM(amount)
        FROM sales
        WHERE LOWER(customer) = LOWER(?)
        """,
        (customer,)
    )

    total = cursor.fetchone()[0] or 0

    print("Customer:", customer)
    print("Total purchase: ₹", total)


# ================= CUSTOMER SEARCH =================

def customer_search():
    customer = input("Customer name: ")

    cursor.execute(
        """
        SELECT date, product, amount
        FROM sales
        WHERE LOWER(customer) = LOWER(?)
        ORDER BY id
        """,
        (customer,)
    )

    sales = cursor.fetchall()

    print("===== Customer Purchases =====")

    if not sales:
        print("Customer nahi mila.")
        return

    for sale in sales:
        date_value, product, amount = sale

        print(
            "Date:", date_value,
            "| Product:", product,
            "| Sale: ₹" + str(amount)
        )


# ================= CUSTOMER REPORT =================

def customer_report():
    customer = input("Customer name: ")

    cursor.execute(
        """
        SELECT date, product, amount
        FROM sales
        WHERE LOWER(customer) = LOWER(?)
        ORDER BY id
        """,
        (customer,)
    )

    sales = cursor.fetchall()

    print("===== Customer Report =====")
    print("Customer:", customer)
    print()

    if not sales:
        print("Customer nahi mila.")
        return

    total = 0

    for sale in sales:
        date_value, product, amount = sale

        print(
            date_value,
            "→",
            product,
            "→ ₹" + str(amount)
        )

        total += amount

    print()
    print("Total purchase: ₹", total)


# ================= PRODUCT REPORT =================

def product_report():
    cursor.execute(
        """
        SELECT product, SUM(quantity), SUM(amount)
        FROM sales
        WHERE quantity IS NOT NULL
        GROUP BY product
        ORDER BY SUM(quantity) DESC
        """
    )

    products = cursor.fetchall()

    print("===== Top Selling Products =====")

    if not products:
        print("Abhi koi quantity wali sale nahi hai.")
        return

    for product, quantity, total in products:
        print(
            product,
            "→",
            quantity,
            "units | ₹" + str(total)
        )

# ================= DATE REPORT =================

def date_report():
    report_date = input("Date (YYYY-MM-DD): ")

    cursor.execute(
        """
        SELECT customer, product, amount
        FROM sales
        WHERE date = ?
        ORDER BY id
        """,
        (report_date,)
    )

    sales = cursor.fetchall()

    print("===== Date Report =====")

    if not sales:
        print("Is date par koi sale nahi mili.")
        return

    total = 0

    for customer, product, amount in sales:
        print(
            customer,
            "→",
            product,
            "→ ₹" + str(amount)
        )

        total += amount

    print("Total Sales: ₹", total)


# ================= DASHBOARD =================

def dashboard():
    today = str(date.today())

    cursor.execute(
        "SELECT SUM(amount) FROM sales WHERE date = ?",
        (today,)
    )
    sales = cursor.fetchone()[0] or 0

    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE date = ?",
        (today,)
    )
    expenses = cursor.fetchone()[0] or 0

    profit = sales - expenses

    cursor.execute(
        "SELECT SUM(quantity) FROM sales WHERE date = ?",
        (today,)
    )
    items_sold = cursor.fetchone()[0] or 0

    print()
    print("===== BUSINESS DASHBOARD =====")
    print()
    print("Date:", today)
    print("Today's Sales: ₹", sales)
    print("Today's Expense: ₹", expenses)
    print("Today's Profit: ₹", profit)
    print("Today's Items Sold:", items_sold)

    print()
    print("Products Sold:")

    cursor.execute(
        """
        SELECT product, SUM(amount)
        FROM sales
        WHERE date = ?
        GROUP BY product
        """,
        (today,)
    )

    products = cursor.fetchall()

    if not products:
        print("Aaj koi product sale nahi hui.")
    else:
        for product, total in products:
            print(product, "→ ₹" + str(total))

    print()
    print("Low Stock Products:")

    cursor.execute(
        "SELECT product, quantity FROM stock WHERE quantity <= 5"
    )

    low_stock = cursor.fetchall()

    if not low_stock:
        print("No low stock products.")
    else:
        for product, quantity in low_stock:
            print(product, "→", quantity)
            print("⚠️ Low Stock:", product)


# ================= BACKUP =================

def backup_data():
    db.commit()
    db.close()

    shutil.copy2("business.db", "business_backup.db")

    print("Database backup successfully ho gaya!")

    global_db_reopen()


def global_db_reopen():
    global db
    global cursor

    db = sqlite3.connect("business.db")
    cursor = db.cursor()

def stock_management():
    cursor.execute("SELECT product, quantity, price FROM stock")
    stock_items = cursor.fetchall()

    print("===== Current Stock =====")

    for product, quantity, price in stock_items:
        print(
            product,
            "→ Quantity:", quantity,
            "| Price: ₹" + str(price)
        )

        if quantity <= 5:
            print("⚠️ Low Stock:", product)


def add_stock():
    product = input("Product name: ")

    while True:
        try:
            quantity = int(input("Quantity add karni hai? "))

            if quantity <= 0:
                print("Quantity 0 se zyada honi chahiye.")
                continue

            break

        except ValueError:
            print("Number likho. Example: 10")

    while True:
        try:
            price = int(input("Selling price: ₹"))

            if price < 0:
                print("Price 0 se kam nahi ho sakti.")
                continue

            break

        except ValueError:
            print("Number likho. Example: 500")

    cursor.execute(
        "SELECT quantity FROM stock WHERE product = ?",
        (product,)
    )

    item = cursor.fetchone()

    if item is not None:
        new_quantity = item[0] + quantity

        cursor.execute(
            "UPDATE stock SET quantity = ?, price = ? WHERE product = ?",
            (new_quantity, price, product)
        )

        print("Existing stock update ho gaya!")

    else:
        cursor.execute(
            "INSERT INTO stock (product, quantity, price) VALUES (?, ?, ?)",
            (product, quantity, price)
        )

        print("Naya product stock me add ho gaya!")

    db.commit()

def update_stock():
    product = input("Product name: ")

    cursor.execute(
        "SELECT quantity, price FROM stock WHERE product = ?",
        (product,)
    )

    item = cursor.fetchone()

    if item is None:
        print("Product stock me nahi mila.")
        return

    print("Current Quantity:", item[0])
    print("Current Price: ₹", item[1])

    while True:
        try:
            quantity = int(input("Kitni quantity add karni hai? "))

            if quantity <= 0:
                print("Quantity 0 se zyada honi chahiye.")
                continue

            break

        except ValueError:
            print("Number likho. Example: 10")

    while True:
        try:
            price = int(input("New selling price: ₹"))

            if price < 0:
                print("Price 0 se kam nahi ho sakti.")
                continue

            break

        except ValueError:
            print("Number likho. Example: 500")

    cursor.execute(
        """
        UPDATE stock
        SET quantity = quantity + ?, price = ?
        WHERE product = ?
        """,
        (quantity, price, product)
    )

    db.commit()

    print("Stock aur price successfully update ho gaye!")


def delete_stock():
    product = input("Kaunsa product delete karna hai? ")

    cursor.execute(
        "SELECT id FROM stock WHERE product = ?",
        (product,)
    )

    item = cursor.fetchone()

    if item is None:
        print("Product stock me nahi mila.")
        return

    cursor.execute(
        "DELETE FROM stock WHERE product = ?",
        (product,)
    )

    db.commit()

    print("Product stock se delete ho gaya!")


# ================= MAIN MENU =================

while True:

    print()
    print("===== Business Assistant =====")
    print("1. Business Dashboard")
    print("2. Sale Add Karo")
    print("3. Expense Add Karo")
    print("4. Aaj Ka Total")
    print("5. Aaj Ka Expense")
    print("6. Aaj Ka Profit")
    print("7. Sales History")
    print("8. Customer Total")
    print("9. Customer Search")
    print("10. Customer Report")
    print("11. Product Report")
    print("12. Date Report")
    print("13. Expense History")
    print("14. Backup Database")
    print("15. Exit")
    print("16. Stock Management")
    print("17. Add Stock")
    print("18. Update Stock")
    print("19. Delete Stock")
    print("20. sale details")
    print("21 .Edit sale")
    print("22. Delete Sale")
    print("23. Quick Sale")
    print("24. Customer History")

    choice = input("Apna option choose karo: ")

    if choice == "1":
        dashboard()

    elif choice == "2":
        add_sale()

    elif choice == "3":
        add_expense()

    elif choice == "4":
        today_total()

    elif choice == "5":
        today_expense()

    elif choice == "6":
        today_profit()

    elif choice == "7":
        sales_history()

    elif choice == "8":
        customer_total()

    elif choice == "9":
        customer_search()

    elif choice == "10":
        customer_report()

    elif choice == "11":
        product_report()

    elif choice == "12":
        date_report()

    elif choice == "13":
        expense_history()

    elif choice == "14":
        backup_data()

    elif choice == "16":
        stock_management()

    elif choice == "17":
        add_stock()

    elif choice == "18":
        update_stock()

    elif choice == "19":
        delete_stock()

    elif choice == "20":
        sale_details()

    elif choice == "21":
        edit_sale()

    elif choice == "22":
        delete_sale()

    elif choice == "23":
        quick_sale()

    elif choice == "24":
        customer_history()

    elif choice == "15":
        print("Bye!")
        break

    else:
        print("Invalid option")


db.close()
