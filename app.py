from flask import Flask, render_template, json, request, redirect, url_for
from flask_mysqldb import MySQL
import os

# Configuration
app = Flask(__name__)
app.config['DEBUG']             = True
app.config['MYSQL_HOST']        = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER']        = 'cs340_ogleja'
app.config['MYSQL_PASSWORD']    = '9706' #last 4 of onid
app.config['MYSQL_DB']          = 'cs340_ogleja'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Routes 
@app.route('/')
def root():
    return render_template("home.html")

@app.route('/employees', methods=["GET"])
def employees():
    cur = mysql.connection.cursor()
    if request.method == "GET":
        query = "select * from Employees;"
        cur.execute(query)
        results = cur.fetchall()
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
        query = f"UPDATE Employees SET first_name = '{fn}', last_name = '{ln}', email = '{email}', dept_id = {dept_id}, active = {active}, hire_date = '{hire_date}', role_id = {role_id} WHERE employee_id = {eid}"
        cur.execute(query)
        mysql.connection.commit()
        return redirect(url_for('employees'))
    if request.method == "GET":
        query = f"select * from Employees where employee_id={id};"
        cur.execute(query)
        results = cur.fetchall()
        return render_template("edit_employee.html", employees=results)
    else:
        query = f"SELECT * FROM Employees WHERE employee_id = %s"
        cur.execute(query, (id,))
        result = cur.fetchall()
        return render_template("edit_employee.html", employees=result)

@app.route("/delete_employee/<int:id>")
def delete_people(id):
    cur = mysql.connection.cursor()
    # mySQL query to delete the person with our passed id
    query = f"DELETE FROM Employees WHERE employee_id = %s;"
    cur.execute(query, (id,))
    mysql.connection.commit()
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
