import os
from flask import Flask, render_template, jsonify
import psycopg2
from dotenv import load_dotenv
from extensions import db
from models import Teacher, Student

load_dotenv()

app = Flask(__name__)

try:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
except Exception as e:
    print(f'Error loading Data Base: {e}')

db.init_app(app)


# with app.app_context():
#     db.create_all()


@app.route('/')
def index():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()