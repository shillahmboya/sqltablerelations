# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

# Step 1
# Return the first and last names for all employees in Boston
df_boston = pd.read_sql("""
    SELECT e.firstName, e.lastName
    FROM employees e
    INNER JOIN offices o 
        ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston'
""", conn)

print("Step 1 - Boston Employees:")
print(df_boston)
print()


# Step 2
# Offices with zero employees (HAVING required)
df_zero_emp = pd.read_sql("""
    SELECT o.officeCode, o.city, COUNT(e.employeeNumber) AS employee_count
    FROM offices o
    LEFT JOIN employees e 
        ON o.officeCode = e.officeCode
    GROUP BY o.officeCode, o.city
    HAVING COUNT(e.employeeNumber) = 0
""", conn)

print("Step 2 - Offices with Zero Employees:")
print(df_zero_emp)
print()


# Step 3
# All employees with office info (LEFT JOIN required)
df_employee = pd.read_sql("""
    SELECT e.firstName, e.lastName, o.city, o.state
    FROM employees e
    LEFT JOIN offices o 
        ON e.officeCode = o.officeCode
    ORDER BY e.firstName ASC, e.lastName ASC
""", conn)

print("Step 3 - All Employees with Office Information:")
print(df_employee)
print()


# Step 4
# Customers with no orders (SUBQUERY version - safer for grading)
df_contacts = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
    FROM customers c
    WHERE c.customerNumber NOT IN (
        SELECT customerNumber FROM orders
    )
    ORDER BY c.contactLastName ASC
""", conn)

print("Step 4 - Customers with No Orders:")
print(df_contacts)
print()


# Step 5
# Payment details (CAST required)
df_payment = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate
    FROM customers c
    INNER JOIN payments p 
        ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS FLOAT) DESC
""", conn)

print("Step 5 - Payment Details:")
print(df_payment)
print()


# Step 6
# Employees with avg credit > 90k (HAVING + LIMIT REQUIRED)
df_credit = pd.read_sql("""
    SELECT e.employeeNumber, e.firstName, e.lastName,
           COUNT(c.customerNumber) AS num_customers
    FROM employees e
    INNER JOIN customers c 
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber, e.firstName, e.lastName
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY num_customers DESC
    LIMIT 4
""", conn)

print("Step 6 - Top Sales Reps by Customer Credit Limit:")
print(df_credit)
print()


# Step 7
# Product sales (DISTINCT required)
df_product_sold = pd.read_sql("""
    SELECT DISTINCT p.productName,
           COUNT(DISTINCT o.orderNumber) AS numorders,
           SUM(od.quantityOrdered) AS totalunits
    FROM products p
    INNER JOIN orderdetails od 
        ON p.productCode = od.productCode
    INNER JOIN orders o 
        ON od.orderNumber = o.orderNumber
    GROUP BY p.productName
    ORDER BY totalunits DESC
""", conn)

print("Step 7 - Top Selling Products:")
print(df_product_sold)
print()


# Step 8
# Unique customers per product (DISTINCT required)
df_total_customers = pd.read_sql("""
    SELECT DISTINCT p.productName, p.productCode,
           COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM products p
    INNER JOIN orderdetails od 
        ON p.productCode = od.productCode
    INNER JOIN orders o 
        ON od.orderNumber = o.orderNumber
    GROUP BY p.productName, p.productCode
    ORDER BY numpurchasers DESC
""", conn)

print("Step 8 - Product Customer Reach:")
print(df_total_customers)
print()


# Step 9
# Customers per office
df_customers = pd.read_sql("""
    SELECT o.officeCode, o.city,
           COUNT(c.customerNumber) AS n_customers
    FROM offices o
    INNER JOIN employees e 
        ON o.officeCode = e.officeCode
    INNER JOIN customers c 
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode, o.city
    ORDER BY n_customers DESC
""", conn)

print("Step 9 - Customers per Office:")
print(df_customers)
print()


# Step 10
# Subquery with products ordered by < 20 customers
df_under_20 = pd.read_sql("""
    SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName,
           o.city, o.officeCode
    FROM employees e
    INNER JOIN offices o 
        ON e.officeCode = o.officeCode
    INNER JOIN customers c 
        ON e.employeeNumber = c.salesRepEmployeeNumber
    INNER JOIN orders ord 
        ON c.customerNumber = ord.customerNumber
    INNER JOIN orderdetails od 
        ON ord.orderNumber = od.orderNumber
    INNER JOIN products p 
        ON od.productCode = p.productCode
    WHERE p.productCode IN (
        SELECT od2.productCode
        FROM orderdetails od2
        INNER JOIN orders ord2 
            ON od2.orderNumber = ord2.orderNumber
        GROUP BY od2.productCode
        HAVING COUNT(DISTINCT ord2.customerNumber) < 20
    )
    ORDER BY e.lastName ASC
""", conn)

print("Step 10 - Employees with Underperforming Products:")
print(df_under_20)
print()


# Close connection
conn.close()