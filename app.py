from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_all_products, add_product, update_product, delete_product, get_product_by_id, get_db_connection

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Home page - Display all products
@app.route('/')
def index():
    products = get_all_products()
    return render_template('index.html', products=products)

# Add a new product
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        
        add_product(name, description, quantity, price)
        flash('Product added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_product.html')

# Edit an existing product
@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit(product_id):
    product = get_product_by_id(product_id)
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        
        update_product(product_id, name, description, quantity, price)
        flash('Product updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit_product.html', product=product)

# Delete a product
@app.route('/delete/<int:product_id>')
def delete(product_id):
    delete_product(product_id)
    flash('Product deleted successfully!', 'danger')
    return redirect(url_for('index'))

@app.route('/search')
def search():
    query = request.args.get('q', '')
    conn = get_db_connection()
    products = conn.execute(
        "SELECT * FROM products WHERE name LIKE ? ORDER BY id DESC",
        (f'%{query}%',)
    ).fetchall()
    conn.close()
    return render_template('index.html', products=products, search_query=query)

if __name__ == '__main__':
    app.run(debug=True)