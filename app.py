# This file uses the starter code from the flask starter app
# Date: 5/25/2023
# Based/Adapted from:
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app

from flask import Flask, render_template, json, request, redirect, url_for
from flask_mysqldb import MySQL
import os

# database connection info
app = Flask(__name__)
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_anderdev"
app.config["MYSQL_PASSWORD"] = "6643"
app.config["MYSQL_DB"] = "cs340_anderdev"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Routes 
@app.route('/')
def root():
    return render_template("home.html")

@app.route('/employees', methods=["GET"])
def employees():
    """
    Render the employees page and pass employee data
    """
    cur = mysql.connection.cursor()
    if request.method == "GET":
        # Retrieve all employees in the database
        query = "SELECT * from Employees;"
        cur.execute(query)
        employees = cur.fetchall()
    return render_template("employees.html", employees=employees)

@app.route('/new_employee', methods=["GET", "POST"])
def new_employee():
    """
    Handles the creation of a new employee.
    
    POST - handle the form submission for creating a new employee
    """
    cur = mysql.connection.cursor()
    if request.method == "POST":
        fn = request.form['first_name']
        ln = request.form['last_name']
        email = request.form['email']
        dept_id = int(request.form['dept_id'])
        active = request.form["active"]
        hire_date = request.form["hire_date"]
        role_id = int(request.form["role_id"])
        query = "INSERT INTO Employees( first_name, last_name, email, dept_id, active, hire_date, role_id )\n"
        vals = f"values ('{fn}', '{ln}', '{email}', {dept_id}, {active}, '{hire_date}', {role_id})"
        cur.execute(query+vals)
        mysql.connection.commit()
        return redirect(url_for('employees'))
    return render_template("new_employee.html")

@app.route('/edit_employee/<int:id>', methods=["GET", "POST"])
def edit_employee(id):
    """
    Handles the editing of an existing employee.
    POST - pushes data of the employee being edited
    GET  - pulls data on the employee being edited
    """
    cur = mysql.connection.cursor()
    if request.method == "POST":
        eid = request.form['employee_id']
        fn = request.form['first_name']
        ln = request.form['last_name']
        email = request.form['email']
        dept_id = int(request.form['dept_id'])
        active = request.form["active"]
        hire_date = request.form["hire_date"]
        role_id = int(request.form["role_id"])
        # UPDATE query
        query = f"UPDATE Employees SET first_name = '{fn}', last_name = '{ln}', email = '{email}', dept_id = {dept_id}, active = {active}, hire_date = '{hire_date}', role_id = {role_id} WHERE employee_id = {eid}"
        # Execute the query to update the employee
        cur.execute(query)
        mysql.connection.commit()
        return redirect(url_for('employees'))
    if request.method == "GET":
        # Render the form for editing an employee
        query = f"SELECT * from Employees WHERE employee_id={id};"
        cur.execute(query)
        employees = cur.fetchall()
        return render_template("edit_employee.html", employees=employees)
    else:
        # Fetch the employee data for displaying in the edit area
        query = f"SELECT * FROM Employees WHERE employee_id = %s"
        cur.execute(query, (id,))
        result = cur.fetchall()
        return render_template("edit_employee.html", employees=result)

@app.route("/delete_employee/<int:id>")
def delete_people(id):
    """
    Route to handle deletion the person with the passed id.
    """
    cur = mysql.connection.cursor()
    # mySQL query to delete the person with our passed id
    query = f"DELETE FROM Employees WHERE employee_id = %s;"
    cur.execute(query, (id,))
    mysql.connection.commit()
    # redirect back to people page
    return redirect(url_for('employees'))

@app.route("/confirm_delete/<int:employee_id>", methods=["GET"])
def confirm_delete(employee_id):
    cur = mysql.connection.cursor()
    query = f"SELECT * FROM Employees WHERE employee_id = %s;"
    cur.execute(query, (employee_id,))
    mysql.connection.commit()
    employee = cur.fetchone()
    print(employee)
    return render_template("confirm_delete.html", employee=employee)

@app.route('/departments')
def departments():
    """
    Renders the departments page
    """
    cur = mysql.connection.cursor()
    if request.method == "GET":
        # Retrieve all departments in the database
        query = "SELECT * from Departments"
        cur.execute(query)
        departments = cur.fetchall()
    return render_template("departments.html", departments=departments)

@app.route('/new_department', methods=["GET", "POST"])
def new_department():
    """
    Handles the creation of a new department.
    
    POST - handle the form submission for creating a new department
    """
    cur = mysql.connection.cursor()
    if request.method == "POST":
        dept_name = request.form["dept_name"]
        manager_id = request.form['manager_employee_id']
        query = "INSERT INTO Departments( dept_name, manager_employee_id )\n"
        vals = f"VALUES ('{dept_name}', '{manager_id}')"
        cur.execute(query+vals)
        mysql.connection.commit()
        return redirect(url_for('departments'))
    else:
        query = "SELECT manager_employee_id FROM Departments"
        cur.execute(query)
        managers = cur.fetchall()
        
        query = f"SELECT DISTINCT d.manager_employee_id, e.first_name, e.last_name FROM Departments d INNER JOIN Employees e ON d.manager_employee_id = e.employee_id"
        cur.execute(query)
        managers = cur.fetchall()
    return render_template("new_department.html", managers=managers)

@app.route('/edit_department/<int:dept_id>', methods=['GET', 'POST'])
def edit_department(dept_id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        dept_name = request.form['dept_name']
        manager_id = request.form['manager_employee_id']
        query = f"UPDATE Departments SET dept_name = '{dept_name}', manager_employee_id = '{manager_id}' WHERE dept_id = {dept_id}"
        cur.execute(query)
        mysql.connection.commit()
        return redirect(url_for('departments')) 
    if request.method == 'GET':
        # Render the form for editing a department
        query = f"SELECT * from Departments WHERE dept_id={dept_id}"
        cur.execute(query)
        departments = cur.fetchall()
        
        # fetch the department details
        query = f"SELECT DISTINCT d.manager_employee_id, e.first_name, e.last_name FROM Departments d INNER JOIN Employees e ON d.manager_employee_id = e.employee_id"
        cur.execute(query)
        managers = cur.fetchall()
        return render_template("edit_department.html", departments=departments, managers=managers)

@app.route('/devices')
def devices():
    """
    Renders the devices page
    """
    # query = ""
    # cursor = db.execute_query(db_connection=db_connection, query=query)
    # results = cursor.fetchall()
    cur = mysql.connection.cursor()
    if request.method == "GET":
        # Retrieve all departments in the database
        query = "SELECT * from Devices"
        cur.execute(query)
        devices = cur.fetchall()
    return render_template("devices.html", devices=devices)

@app.route('/new_device', methods=['GET', 'POST'])
def new_device():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        device_name = request.form['device_name']
        type = request.form['type']
        access_level = int(request.form['access_level'])
        usb_access = request.form['usb_access']
        employee_id = int(request.form['employee_id'])
        query = "INSERT INTO Devices( device_name, type, access_level, usb_access, employee_id )\n"
        vals = f"values ('{device_name}', '{type}', {access_level}, '{usb_access}', {employee_id})"
        cur.execute(query+vals)
        mysql.connection.commit()
        return redirect(url_for('devices'))
    
    return render_template("new_device.html")

@app.route('/roles')
def roles():
    # query = ""
    # cursor = db.execute_query(db_connection=db_connection, query=query)
    # results = cursor.fetchall()
    cur = mysql.connection.cursor()
    if request.method == "GET":
        query = "SELECT * FROM Roles"
        cur.execute(query)
        roles=cur.fetchall()
    return render_template("roles.html", roles=roles)

@app.route('/new_role', methods=['GET', 'POST'])
def new_role():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        title = request.form['title']
        access_level = request.form['access_level']
        query = "INSERT INTO Roles( title, access_level )\n"
        vals = f"values ('{title}', '{access_level}')"
        cur.execute(query+vals)
        mysql.connection.commit()
        return redirect(url_for('roles'))
    
    return render_template("new_role.html")

@app.route("/delete_role/<int:id>")
def delete_role(id):
    """
    Route to handle deleting a role with the passed id.
    """
    cur = mysql.connection.cursor()
    # mySQL query to delete the person with our passed id
    query = f"DELETE FROM Roles WHERE role_id = %s;"
    cur.execute(query, (id,))
    mysql.connection.commit()
    # redirect back to people page
    return redirect(url_for('roles'))

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
    port = int(os.environ.get('PORT', 11328))
    app.run(port=port, debug=True)
