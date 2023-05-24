from unittest import result
from flask import Flask, render_template, json, request, redirect, url_for
import os
import database.db_connector as db
import sys
# Configuration

app = Flask(__name__)
try:
    db_connection = db.connect_to_database()
except RuntimeError:
    print("Error connecting to the database")
    sys.exit(-1)

# Routes 
@app.route('/')
def root():
    return render_template("home.html")

@app.route('/employees', methods=["GET"])
def employees():
    if request.method == "GET":
        query = "select * from Employees;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
    return render_template("employees.html", employees=results)

@app.route('/departments')
def departments():
    # query = ""
    # cursor = db.execute_query(db_connection=db_connection, query=query)
    # results = cursor.fetchall()
    return render_template("departments.html")

@app.route('/devices')
def devices():
    # query = ""
    # cursor = db.execute_query(db_connection=db_connection, query=query)
    # results = cursor.fetchall()
    return render_template("devices.html")

@app.route('/new_employee', methods=["GET", "POST"])
def new_employee():
    if request.method == "POST":
        fn = request.form['first_name']
        ln = request.form['last_name']
        email = request.form['email']
        dept_id = int(request.form['dept_id'])
        active = 1 if request.form["active"] == 'on' else 0
        hire_date = request.form["hire_date"]
        role_id = int(request.form["role_id"])
        query = "INSERT INTO Employees( first_name, last_name, email, dept_id, active, hire_date, role_id )\n"
        vals = f"values ('{fn}', '{ln}', '{email}', {dept_id}, {active}, '{hire_date}', {role_id})"
        cursor = db.execute_query(db_connection=db_connection, query=(query+vals))
        return redirect(url_for('employees'))
    return render_template("new_employee.html")

@app.route('/edit_employee/<int:id>', methods=["GET", "POST"])
def edit_employee(id):
    if request.method == "POST":
        eid = request.form['employee_id']
        fn = request.form['first_name']
        ln = request.form['last_name']
        email = request.form['email']
        dept_id = int(request.form['dept_id'])
        active = 1 if request.form["active"] == 'on' else 0
        role_id = int(request.form["role_id"])
        query = f"UPDATE Employees SET first_name = '{fn}', last_name = '{ln}', email = '{email}', dept_id = {dept_id}, active = {active}, role_id = {role_id} WHERE employee_id = {eid}"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        return redirect(url_for('employees'))
    if request.method == "GET":
        query = f"select * from Employees where employee_id={id};"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("edit_employee.html", employees=results)
    else:
        query = f"SELECT * FROM Employees WHERE employee_id = {id}"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        result = cursor.fetchall()
        return render_template("edit_employee.html", employees=result)

@app.route("/delete_employee/<int:id>")
def delete_people(id):
    # mySQL query to delete the person with our passed id
    query = f"DELETE FROM Employees WHERE employee_id = {id};"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    # redirect back to people page
    return redirect(url_for('employees'))

@app.route('/roles')
def roles():
    # query = ""
    # cursor = db.execute_query(db_connection=db_connection, query=query)
    # results = cursor.fetchall()
    return render_template("roles.html")

@app.route('/trainings')
def trainings():
    # query = ""
    # cursor = db.execute_query(db_connection=db_connection, query=query)
    # results = cursor.fetchall()
    return render_template("trainings.html")

@app.route('/passwords')
def passwords():
    # query = ""
    # cursor = db.execute_query(db_connection=db_connection, query=query)
    # results = cursor.fetchall()
    return render_template("passwords.html")

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9113))
    app.run(port=port, debug=True)
