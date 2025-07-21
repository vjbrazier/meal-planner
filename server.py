"""
The Server file. Hosts the server.
"""
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """
    The index page.
    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)
