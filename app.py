from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)

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

@app.route('/')
def home():
    return render_template('hello.html')

@app.route('/products/list')
def list_products():
    cursor = g.db.cursor()
    cursor.execute('SELECT * FROM products')
    productos = cursor.fetchall()
    return render_template('/products/list.html', products=productos)

if __name__ == '__main__':
    app.run()