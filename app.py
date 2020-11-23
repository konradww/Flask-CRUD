from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import psycopg2


app = Flask(__name__)
# app.secret_key = "Secret Key"
app.debug = True
app.config['SECRET_KEY'] = 'a really really really really long secret key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:MYsql123*@localhost:5433/database_flaskapp'
try:
    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='postgres', pw='MYsql123*', url='127.0.0.1', db='database_flaskapp')
except:
    print ("error")
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning


db = SQLAlchemy(app)


class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    def __repr__(self, db):
        return '<USER %r>'


@app.route('/insert', methods=['POST'])
def insert():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        my_data = Employees(name, email, phone)
        db.session.add(my_data)
        db.session.commit()
        flash("Employee Inserted Successfully")

    return redirect(url_for('Index'))


# this is our update route where we are going to update our employee
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Employees.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']

        db.session.commit()
        flash("Employee Updated Successfully")

        return redirect(url_for('Index'))


# This route is for deleting our employee
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Employees.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")

    return redirect(url_for('Index'))

@app.route('/')
def Index():

    all_data = Employees.query.all()
    return render_template("index.html", employees = all_data)


if __name__ == "__main__":
    app.run(debug=True)