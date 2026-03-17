# app.py (or index.py/server.py)
from flask import Flask

app = Flask(__name__)  # Must be named 'app'

@app.route('/')
def home():
    return 'Hello, World!'