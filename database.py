import sqlite3

DATABASE = 'inventory.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

def init_db():
    """Create the products table if it doesn't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_all_products():
    """Return all products from the database"""
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products ORDER BY id DESC').fetchall()
    conn.close()
    return products

def get_product_by_id(product_id):
    """Return a single product by ID"""
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    return product

def add_product(name, description, quantity, price):
    """Add a new product to the database"""
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO products (name, description, quantity, price) VALUES (?, ?, ?, ?)',
        (name, description, quantity, price)
    )
    conn.commit()
    conn.close()

def update_product(product_id, name, description, quantity, price):
    """Update an existing product"""
    conn = get_db_connection()
    conn.execute(
        'UPDATE products SET name = ?, description = ?, quantity = ?, price = ? WHERE id = ?',
        (name, description, quantity, price, product_id)
    )
    conn.commit()
    conn.close()

def delete_product(product_id):
    """Delete a product from the database"""
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()

init_db()