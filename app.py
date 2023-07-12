# This file is all based on the CS 340 starter code, with the exception of added route handlers and join queries
# Date: 5/25/2023
# Based/Adapted from:
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app

from flask import Flask, render_template, json, request, redirect, url_for
from flask_mysqldb import MySQL
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create Flask app
app = Flask(__name__, static_folder='static')

# Configure MySQL connection
app.config["MYSQL_HOST"] = os.environ.get("DB_HOST")
app.config["MYSQL_USER"] = os.environ.get("DB_USER")
app.config["MYSQL_PASSWORD"] = os.environ.get("DB_PASSWORD")
app.config["MYSQL_DB"] = os.environ.get("DB_NAME")
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
    This section uses aliases
    Date: 6/5/23
    Adapted from:
    Source URL: https://www.w3schools.com/sql/sql_alias.asp
    """
    cur = mysql.connection.cursor()
    if request.method == "GET":
        # Retrieve employees using left join to get dept_name and title instead of ID and ensure all employees are included even if they aren't assigned a role/department
        query = "SELECT e.employee_id, e.first_name, e.last_name, e.email, d.dept_name, r.title, e.active, e.hire_date FROM Employees e LEFT JOIN Departments d ON e.dept_id = d.dept_id LEFT JOIN Roles r ON e.role_id = r.role_id;"
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
        active = request.form['active']
        hire_date = request.form["hire_date"]
        role_id = int(request.form["role_id"])
        query = "INSERT INTO Employees( first_name, last_name, email, dept_id, active, hire_date, role_id )\n"
        vals = f"values ('{fn}', '{ln}', '{email}', {dept_id}, '{active}', '{hire_date}', '{role_id}')"
        cur.execute(query+vals)
        mysql.connection.commit()
        return redirect(url_for('employees'))
    
    if request.method == "GET":
        query = "SELECT dept_id, dept_name FROM Departments;"
        cur.execute(query)
        departments = cur.fetchall()
        
        query = "SELECT role_id, title FROM Roles;"
        cur.execute(query)
        roles = cur.fetchall()
    return render_template("new_employee.html", departments=departments, roles=roles)

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
        active = request.form['active']
        hire_date = request.form["hire_date"]
        role_id = int(request.form["role_id"]) 
               
        # UPDATE query
        query = f"UPDATE Employees SET first_name = '{fn}', last_name = '{ln}', email = '{email}', dept_id = {dept_id}, active = '{active}', hire_date = '{hire_date}', role_id = {role_id} WHERE employee_id = {eid}"
        
        # Execute the query to update the employee
        cur.execute(query)
        mysql.connection.commit()
        return redirect(url_for('employees'))
    
    if request.method == "GET":
        # Retrieve employees using left join to get dept_name and title instead of ID and ensure all employees are included even if they aren't assigned a role/department
        query = f"SELECT e.employee_id, e.first_name, e.last_name, e.email, e.dept_id, e.active, e.hire_date, r.role_id, r.title, d.dept_id, d.dept_name FROM Employees e LEFT JOIN Departments d ON e.dept_id = d.dept_id LEFT JOIN Roles r ON e.role_id = r.role_id WHERE employee_id={id};"
        cur.execute(query)
        employees = cur.fetchall()
        
        # retrieve dept name associated with id
        query = "SELECT dept_id, dept_name FROM Departments;"
        cur.execute(query)
        departments = cur.fetchall()
        
        # retrieve title associated with id
        query = "SELECT role_id, title FROM Roles;"
        cur.execute(query)
        roles = cur.fetchall()
        return render_template("edit_employee.html", employees=employees, departments=departments, roles=roles)

@app.route("/delete_employee/<int:id>", methods=["POST"])
def delete_people(id):
    """
    Route to handle deletion the person with the passed id.
    """
    cur = mysql.connection.cursor()
    # mySQL query to delete the person with our passed id
    query = f"DELETE FROM Employees WHERE employee_id = %s;"
    cur.execute(query, (id,))
    mysql.connection.commit()
    # redirect back to employee page
    return redirect(url_for('employees'))

@app.route("/confirm_delete/<int:id>", methods=["GET"])
def confirm_delete(id):
    """
    Route to confirm deletion of employee
    """
    cur = mysql.connection.cursor()
    
    # Retrieve employee using left join to get dept_name and title instead of ID
    query = "SELECT e.employee_id, e.first_name, e.last_name, e.email, d.dept_name, r.title, e.active, e.hire_date FROM Employees e LEFT JOIN Departments d ON e.dept_id = d.dept_id LEFT JOIN Roles r ON e.role_id = r.role_id WHERE e.employee_id = %s;"
    cur.execute(query, (id,))
    employee = cur.fetchone()
    
    # retrieve dept name associated with id
    query = "SELECT dept_id, dept_name FROM Departments;"
    cur.execute(query)
    department = cur.fetchone()
    
    # retrieve title associated with id
    query = "SELECT role_id, title FROM Roles;"
    cur.execute(query)
    role = cur.fetchone()
    return render_template("confirm_delete.html", employee=employee, department=department, role=role)

@app.route('/departments')
def departments():
    """
    Renders the departments page
    """
    cur = mysql.connection.cursor()
    if request.method == "GET":
        # Retrieve departments using a left join to show manager's name instead of ID - show all departments even if they don't have a manager
        query = "SELECT d.dept_id, d.dept_name, e.first_name, e.last_name FROM Departments d LEFT JOIN Employees e ON d.manager_employee_id = e.employee_id;"
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
        
        # set manager_id to NULL if None is selected from dropdown
        if not manager_id:
            query = "INSERT INTO Departments (dept_name, manager_employee_id) VALUES (%s, NULL);"
            values = (dept_name,)
        else:
            query = "INSERT INTO Departments (dept_name, manager_employee_id) VALUES (%s, %s);"
            values = (dept_name, manager_id)
            
        cur.execute(query, values)
        managers = cur.fetchall()
        mysql.connection.commit()
        return redirect(url_for('departments'))
    else:
        query = "SELECT employee_id, first_name, last_name FROM Employees"
        cur.execute(query)
        managers = cur.fetchall()
    return render_template("new_department.html", managers=managers)

@app.route('/edit_department/<int:dept_id>', methods=['GET', 'POST'])
def edit_department(dept_id):
    """
    Route to edit a particular department
    """
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        dept_name = request.form['dept_name']
        manager_id = request.form['manager_employee_id']
        
        # Set manager_id to NULL if None is selected from dropdown
        if not manager_id:
            query = f"UPDATE Departments SET dept_name = %s, manager_employee_id = NULL WHERE dept_id = %s;"
            values = (dept_name, dept_id)
        else:
            # update manager_employee_id with provided value
            query = f"UPDATE Departments SET dept_name = %s, manager_employee_id = %s WHERE dept_id = %s;"
            values = (dept_name, manager_id, dept_id)
        
        cur.execute(query, values)
        mysql.connection.commit()
        return redirect(url_for('departments')) 
    
    if request.method == 'GET':
        # Retrieve departments using left join to get first_name and last_name instead of ID and ensure all departments are included even if they aren't assigned to an employee
        query = f"SELECT DISTINCT d.dept_id, d.dept_name, d.manager_employee_id, e.first_name, e.last_name FROM Departments d LEFT JOIN Employees e ON d.manager_employee_id = e.employee_id WHERE d.dept_id = %s;"
        cur.execute(query, (dept_id,))
        departments = cur.fetchall()  
 
        # Fetch all employees for the dropdown
        query = "SELECT employee_id, first_name, last_name FROM Employees;"
        cur.execute(query)
        employees = cur.fetchall()
        return render_template("edit_department.html", departments=departments, employees=employees)
    
@app.route("/delete_department/<int:id>")
def delete_department(id):
    """
    Route to handle deleting a department with the passed id.
    """
    cur = mysql.connection.cursor()
    # mySQL query to delete the department with passed id
    query = f"DELETE FROM Departments WHERE dept_id = %s;"
    cur.execute(query, (id,))
    mysql.connection.commit()
    # redirect back to departments page
    return redirect(url_for('departments'))

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
        # Retrieve devices using left join to get first_name and last_name instead of ID and ensure all devices are included even if they aren't assigned to an employee
        query = "SELECT d.device_id, d.device_name, d.type, d.access_level, d.usb_access, e.first_name, e.last_name from Devices d LEFT JOIN Employees e ON d.employee_id = e.employee_id;"
        cur.execute(query)
        devices = cur.fetchall()
    return render_template("devices.html", devices=devices)

@app.route('/new_device', methods=['GET', 'POST'])
def new_device():
    """
    Route to add a new device
    """
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
    
    query = f"SELECT employee_id, first_name, last_name FROM Employees;"
    cur.execute(query)
    employees= cur.fetchall()
    
    return render_template("new_device.html", employees=employees)

@app.route("/delete_device/<int:id>")
def delete_device(id):
    """
    Route to handle deleting a device with the passed id.
    """
    cur = mysql.connection.cursor()
    # mySQL query to delete the person with our passed id
    query = f"DELETE FROM Devices WHERE device_id = %s;"
    cur.execute(query, (id,))
    mysql.connection.commit()
    # redirect back to people page
    return redirect(url_for('devices'))

@app.route('/roles')
def roles():
    """
    Render the roles page 
    """
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
    """
    Route to add a new role
    """
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

@app.route('/edit_role/<int:id>', methods=['GET', 'POST'])
def edit_role(id):
    """
    Route to edit a particular department
    """
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        title = request.form['title']
        access_level = int(request.form['access_level'])
        query = f"UPDATE Roles SET title = '{title}',  access_level = {access_level} WHERE role_id = %s"
        cur.execute(query, (id,))
        mysql.connection.commit()
        return redirect(url_for('roles'))  

    query = "SELECT * FROM Roles WHERE role_id = %s"
    cur.execute(query, (id,))
    roles = cur.fetchall()
    
    query = f"SELECT DISTINCT title FROM Roles"
    cur.execute(query)
    title = cur.fetchone() 
    return render_template("edit_role.html", roles=roles, title=title)

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

@app.route('/trainings', methods=['GET', 'POST'])
def trainings():
    """
    Route to handle both the display of all training + training details
    Also allows users to create new training + training details or 
    delete existing.
    """
    
    if request.method == 'GET':
        # Grab all trainings
        cur = mysql.connection.cursor()  
        query = "SELECT * FROM Trainings;"
        cur.execute(query)
        trainings_res = cur.fetchall()
        
        # Retrieve trainings using join to get title, first, and last name instead of IDs
        query = "SELECT td.training_details_id, td.employee_id, td.training_id, td.completion_date, td.pass_or_fail, e.first_name, e.last_name, t.title FROM TrainingDetails td JOIN Employees e ON td.employee_id = e.employee_id JOIN Trainings t ON td.training_id = t.training_id;"
        cur.execute(query)
        training_details_res = cur.fetchall()
        
        # retrieve all trainings to populate dropdown
        query = "SELECT training_id, title FROM Trainings;"
        cur.execute(query)
        training_titles = cur.fetchall()
        
        # grab all employees
        query = "SELECT employee_id, first_name, last_name FROM Employees;"
        cur.execute(query)
        employees = cur.fetchall()
        return render_template("trainings.html", trainings=trainings_res, training_details=training_details_res, training_titles=training_titles, employees=employees)    
    
    if request.method == 'POST':    
        # check if coming from trainings or training log
        if request.form['form_type'] == "new_train":
            cur = mysql.connection.cursor()
            title = request.form['title']
            duration_in_min = request.form['duration_in_min']
            required_status = request.form['required_status'] 
            query = "INSERT INTO Trainings (title, duration_in_min, required_status) VALUES (%s, %s, %s)"
            vals = (title, duration_in_min, required_status)
            cur.execute(query, vals)
            mysql.connection.commit()
        
        if request.form['form_type'] == "new_train_log":
            cur = mysql.connection.cursor()
            employee_id = request.form['employee_id']
            training_id = request.form['training_id']
            completion_date = request.form['completion_date']
            pass_or_fail = request.form['pass_or_fail']
            query = "INSERT INTO TrainingDetails (employee_id, training_id, completion_date, pass_or_fail) VALUES (%s, %s, %s, %s)"
            vals = (employee_id, training_id, completion_date, pass_or_fail)
            cur.execute(query, vals)
            mysql.connection.commit()
        
        return redirect(url_for('trainings'))

@app.route("/edit_train_log/<int:id>", methods=['GET', 'POST'])
def edit_train_log(id):
    """
    Route to handle editing a training log
    """
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        training_id = request.form['training_id']
        completion_date = request.form['completion_date']
        pass_or_fail = request.form['pass_or_fail']
        
        # update training details
        query = "UPDATE TrainingDetails SET employee_id = %s, training_id = %s, completion_date = %s, pass_or_fail = %s WHERE training_details_id = %s"
        vals = (employee_id, training_id, completion_date, pass_or_fail, id)
        cur.execute(query, vals)
        mysql.connection.commit()
        
        return redirect(url_for('trainings'))

    if request.method == 'GET':
        # Retrieve trainings using join to get title, first, and last name instead of displaying IDs
        query = "SELECT td.training_details_id, td.employee_id, td.training_id, td.completion_date, td.pass_or_fail, e.first_name, e.last_name, t.title FROM TrainingDetails td JOIN Employees e ON td.employee_id = e.employee_id JOIN Trainings t ON td.training_id = t.training_id WHERE td.training_details_id = %s;"
        cur.execute(query, (id,))
        training_details = cur.fetchone()

        # Retrieve all trainings to populate dropdown
        query = "SELECT training_id, title FROM Trainings;"
        cur.execute(query)
        trainings = cur.fetchall()

        # Retrieve all employees to populate dropdown
        query = "SELECT DISTINCT employee_id, first_name, last_name FROM Employees;"
        cur.execute(query)
        employees = cur.fetchall()

        return render_template('edit_train_log.html', training_details=training_details, trainings=trainings, employees=employees)

@app.route("/delete_training/<int:id>")
def delete_training(id):
    """
    Route to handle deleting a training item with the passed id.
    """
    cur = mysql.connection.cursor()
    # mySQL query to delete the person with our passed id
    query = f"DELETE FROM Trainings where training_id = %s;"
    cur.execute(query, (id,))
    mysql.connection.commit()
    # redirect back to people page
    return redirect(url_for('trainings'))

@app.route("/delete_training_log/<int:id>")
def delete_training_log(id):
    """
    Route to handle deleting a training log with the passed id.
    """
    cur = mysql.connection.cursor()
    # mySQL query to delete the person with our passed id
    query = f"DELETE FROM TrainingDetails WHERE training_id = %s;"
    cur.execute(query, (id,))
    mysql.connection.commit()
    # redirect back to people page
    return redirect(url_for('trainings'))


@app.route('/passwords', methods=['GET', 'POST'])
def passwords():
    """
    Render the passwords page 
    """
    cur = mysql.connection.cursor()     
    if request.method == 'POST':
        # check if coming from trainings or training log
        if request.form['form_type'] == "new_password":
            password = request.form['password']
            req_change = request.form['req_change'] 
            eid = int(request.form['employee_id'])
            query = "INSERT INTO Passwords (password, req_change, employee_id)"
            vals = f"VALUES ('{password}', '{req_change}', {eid});"
            cur.execute(query+vals)
            mysql.connection.commit()
            
    # retrieve passwords using join to display first and last name of employee instead of ID
    query = "SELECT p.password_id, p.password, p.req_change, e.first_name, e.last_name FROM Passwords p JOIN Employees e ON p.employee_id = e.employee_id;"
    cur.execute(query)
    passwords=cur.fetchall()
    
    # retrieve all employees first and last name to populate for dropdown option
    query = f"SELECT employee_id, first_name, last_name FROM Employees;"
    cur.execute(query)
    employees = cur.fetchall()
    return render_template("passwords.html", passwords=passwords, employees=employees)

@app.route("/delete_password/<int:id>")
def delete_password(id):
    """
    Route to handle deleting a training item with the passed id.
    """
    cur = mysql.connection.cursor()
    # mySQL query to delete the person with our passed id
    query = f"DELETE FROM Passwords where password_id = %s;"
    cur.execute(query, (id,))
    mysql.connection.commit()
    # redirect back to people page
    return redirect(url_for('passwords'))


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 11328))
    app.run(port=port, debug=True)
