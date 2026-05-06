# CodeGrade step0
# Run this cell without changes

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# CodeGrade step1
# Step 1
# Return the first and last names for all employees in Boston

df_boston = pd.read_sql("""
    SELECT e.firstName, e.lastName
    FROM employees e
    JOIN offices o ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston'
""", conn)

print("Step 1 - Boston Employees:")
print(df_boston)
print()


# CodeGrade step2
# Step 2
# Are there any offices that have zero employees?

df_zero_emp = pd.read_sql("""
    SELECT o.officeCode, o.city, COUNT(e.employeeNumber) AS employee_count
    FROM offices o
    LEFT JOIN employees e ON o.officeCode = e.officeCode
    GROUP BY o.officeCode, o.city
    HAVING COUNT(e.employeeNumber) = 0
""", conn)

print("Step 2 - Offices with Zero Employees:")
print(df_zero_emp)
print()


# CodeGrade step3
# Step 3
# Return employees first name and last name along with the city and state of their office
# Include all employees and order by first name, then last name

df_employee = pd.read_sql("""
    SELECT e.firstName, e.lastName, o.city, o.state
    FROM employees e
    LEFT JOIN offices o ON e.officeCode = o.officeCode
    ORDER BY e.firstName ASC, e.lastName ASC
""", conn)

print("Step 3 - All Employees with Office Information:")
print(df_employee)
print()


# CodeGrade step4
# Step 4
# Return customer contact information (first name, last name, phone number)
# and their sales rep's employee number for customers with no orders
# Sort alphabetically by last name

df_contacts = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
    FROM customers c
    LEFT JOIN orders o ON c.customerNumber = o.customerNumber
    WHERE o.orderNumber IS NULL
    ORDER BY c.contactLastName ASC
""", conn)

print("Step 4 - Customers with No Orders:")
print(df_contacts)
print()


# CodeGrade step5
# Step 5
# Return customer contacts (first and last names) along with payment amount and date
# Sort in descending order by payment amount
# Use CAST to ensure amount is treated as numeric

df_payment = pd.read_sql("""
    SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate
    FROM customers c
    JOIN payments p ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC
""", conn)

print("Step 5 - Payment Details:")
print(df_payment)
print()


# CodeGrade step6
# Step 6
# Return employee number, first name, last name, and number of customers
# for employees whose customers have average credit limit over 90k
# Sort by number of customers from high to low (top 4)

df_credit = pd.read_sql("""
    SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS num_customers
    FROM employees e
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY e.employeeNumber, e.firstName, e.lastName
    HAVING AVG(c.creditLimit) > 90000
    ORDER BY num_customers DESC
    LIMIT 4
""", conn)

print("Step 6 - Top Sales Reps by Customer Credit Limit:")
print(df_credit)
print()


# CodeGrade step7
# Step 7
# Return product name, count of orders (numorders), and total quantity sold (totalunits)
# Sort by totalunits highest to lowest

df_product_sold = pd.read_sql("""
    SELECT p.productName,
           COUNT(DISTINCT o.orderNumber) AS numorders,
           SUM(od.quantityOrdered) AS totalunits
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    JOIN orders o ON od.orderNumber = o.orderNumber
    GROUP BY p.productName
    ORDER BY totalunits DESC
""", conn)

print("Step 7 - Top Selling Products:")
print(df_product_sold)
print()


# CodeGrade step8
# Step 8
# Return product name, product code, and number of unique customers (numpurchasers)
# Sort by highest number of purchasers

df_total_customers = pd.read_sql("""
    SELECT p.productName, p.productCode, COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM products p
    JOIN orderdetails od ON p.productCode = od.productCode
    JOIN orders o ON od.orderNumber = o.orderNumber
    GROUP BY p.productName, p.productCode
    ORDER BY numpurchasers DESC
""", conn)

print("Step 8 - Product Customer Reach:")
print(df_total_customers)
print()


# CodeGrade step9
# Step 9
# Return office code, city, and count of customers (n_customers)

df_customers = pd.read_sql("""
    SELECT o.officeCode, o.city, COUNT(c.customerNumber) AS n_customers
    FROM offices o
    JOIN employees e ON o.officeCode = e.officeCode
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY o.officeCode, o.city
""", conn)

print("Step 9 - Customers per Office:")
print(df_customers)
print()


# CodeGrade step10
# Step 10
# Using a subquery, find employees who sold products that have been ordered by fewer than 20 customers
# Return employee number, first name, last name, office city, and office code
# Sort alphabetically by last name

df_under_20 = pd.read_sql("""
    SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, o.city, o.officeCode
    FROM employees e
    JOIN offices o ON e.officeCode = o.officeCode
    JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN orders ord ON c.customerNumber = ord.customerNumber
    JOIN orderdetails od ON ord.orderNumber = od.orderNumber
    WHERE od.productCode IN (
        SELECT od2.productCode
        FROM orderdetails od2
        JOIN orders ord2 ON od2.orderNumber = ord2.orderNumber
        GROUP BY od2.productCode
        HAVING COUNT(DISTINCT ord2.customerNumber) < 20
    )
    ORDER BY e.lastName ASC
""", conn)

print("Step 10 - Employees with Underperforming Products:")
print(df_under_20)
print()


# Run this cell without changes
conn.close()
