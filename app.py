import os
from flask import Flask, render_template, jsonify
import psycopg2
from dotenv import load_dotenv
from extensions import db
from models import Teacher, Student


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'db', 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def index():
    return render_template('home.html')


if __name__ == '__main__':
    # Create the 'db' directory if it doesn't exist
    db_dir = os.path.join(os.getcwd(), 'db')
    os.makedirs(db_dir, exist_ok=True)

    # Create the database tables
    with app.app_context():
        db.create_all()

    # Run the Flask application
    app.run(debug=True)