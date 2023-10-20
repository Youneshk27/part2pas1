from flask import Flask, render_template, g, request, redirect, url_for, flash, abort
import sqlite3

app = Flask(__name__)

app.secret_key = 'alumne'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('database.db')
    return db

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Ruta para la página de inicio
@app.route('/')
def home():
    return render_template('hello.html')

# Ruta para listar productos
@app.route('/products/list')
def list_products():
    cursor = g.db.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    return render_template('products/list.html', products=products)

# Ruta para crear un nuevo producto
@app.route('/products/create', methods=["GET", "POST"])
def products_create():
    if request.method == 'GET':
        return render_template('products/create.html')
    elif request.method == 'POST':
        # Obtener los datos del formulario
        title = request.form['title']
        description = request.form['description']
        price = float(request.form['price'])
        
        # Aquí deberías validar los datos y guardarlos en la base de datos
        cursor = g.db.cursor()
        cursor.execute('INSERT INTO products (title, description, price) VALUES (?, ?, ?)', (title, description, price))
        g.db.commit()
        
        flash("Producto creado con éxito")
        return redirect(url_for('list_products'))
    else:
        abort(404)

# Ruta para actualizar un producto existente
@app.route('/products/update/<int:id>', methods=["GET", "POST"])
def products_update(id):
    cursor = g.db.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (id,))
    product = cursor.fetchone()
    if product is None:
        abort(404)

    if request.method == 'GET':
        # Obtén la lista de categorías de la base de datos
        cursor.execute('SELECT * FROM categories')
        categories = cursor.fetchall()
        return render_template('products/update.html', product=product, categories=categories)
    elif request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = float(request.form['price'])
        category_id = request.form['category_id']
        
        # Aquí deberías validar los datos y actualizarlos en la base de datos
        cursor.execute('UPDATE products SET title = ?, description = ?, price = ?, category_id = ? WHERE id = ?', (title, description, price, category_id, id))
        g.db.commit()
        
        flash("Producto actualizado con éxito")
        return redirect(url_for('list_products'))
    else:
        abort(404)

if __name__ == '__main':
    app.run()