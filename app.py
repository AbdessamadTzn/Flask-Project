import os
from flask import Flask, render_template, jsonify
import psycopg2
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
try:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
except Exception as e:
    print(f'Error loading Data Base: {e}')



@app.route('/')
def index():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()