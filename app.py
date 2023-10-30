import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///abdessamd.db"

#TODO: define models
#handle api hyaa lwal o dwzhaa l front end
@app.route("/")
def index():
    return render_template('home.html')
@app.route("/student")
def student():
    return render_template('studentlist.html')

if __name__ == '__main__':
    app.run(debug=True)

    ##window.localstorage //for logins 