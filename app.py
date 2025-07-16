from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create the database and table if not exists
def init_db():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products')
    items = c.fetchall()
    conn.close()
    return render_template('index.html', products=items)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    item = c.fetchone()
    conn.close()
    return render_template('product.html', product=item)

@app.route('/add', methods=['POST'])
def add_product():
    name = request.form['name']
    price = float(request.form['price'])
    description = request.form['description']
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('INSERT INTO products (name, price, description) VALUES (?, ?, ?)',
              (name, price, description))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)