from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/init')
def init():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()