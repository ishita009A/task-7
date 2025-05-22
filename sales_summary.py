
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to SQLite database
conn = sqlite3.connect('sales_data.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        product TEXT,
        quantity INTEGER,
        price REAL
    )
''')

# Insert data
sales_data = [
    ('Apple', 10, 0.5),
    ('Banana', 20, 0.3),
    ('Orange', 15, 0.4),
    ('Apple', 5, 0.5),
    ('Banana', 10, 0.3),
    ('Orange', 10, 0.4)
]

cursor.execute('DELETE FROM sales')
cursor.executemany('INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)', sales_data)
conn.commit()

# Query
query = '''
    SELECT product, 
           SUM(quantity) AS total_qty, 
           SUM(quantity * price) AS revenue 
    FROM sales 
    GROUP BY product
'''

df = pd.read_sql_query(query, conn)
conn.close()

# Output
print(df)

# Plot
df.plot(kind='bar', x='product', y='revenue', legend=False, title='Revenue by Product')
plt.ylabel("Revenue ($)")
plt.tight_layout()
plt.savefig("sales_chart.png")
plt.show()
