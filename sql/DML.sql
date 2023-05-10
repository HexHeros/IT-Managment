-- Employees
SELECT * FROM Employees; -- select all Employees

SELECT Employees.first_name, Employees.last_name, Roles.title -- Gives a list of software engineers that are active 
FROM Employees
INNER JOIN Roles
ON Roles.role_id = Employees.role_id
WHERE Roles.role_id = 1 and Employees.active = True;

-- add a new employee
INSERT INTO Employees(first_name, last_name, email, dept_id, active, hire_date, role_id)
VALUES  (:first_nameInput, :last_nameInput, :emailInput, :dept_idInput, :activeInput, :hire_dateInput, :role_id_from_the_dropdown_Input);

DELETE FROM Employees WHERE employee_id = :employee_id_selected_from_employees_page; -- delete selected employee

-- update a Employees's data based on submission of the Update Employee form 
UPDATE Employees SET first_name = :first_nameInput, last_name= :last_nameInput, email = :emailInput, dept_id= :dept_idInput WHERE id= :employee_ID_from_the_update_form;

-- Departments
SELECT * FROM Departments; -- select all Departments

-- add a new department
INSERT INTO Departments (dept_name, manager_employee_id)
VALUES (:dept_nameInput, :manager_employee_id_from_dropdown_Input);

-- update a Department's manager based on submission of the Update form
UPDATE Departments SET manager_employee_id = :new_emp_id; 

UPDATE Departments SET manager_employee_id = NULL; -- Nullify the current manager

-- Roles
SELECT * FROM Roles; -- select all Roles

-- add a new role
INSERT INTO Roles (title, access_level)
VALUES (:titleInput, :access_levelInput);

-- Devices
SELECT * FROM Devices; -- selelct all Devices

-- add a new device
INSERT INTO Devices (device_name, type, access_level, usb_access, employee_id)
VALUES (:device_nameInput, :typeInput, :access_levelInput, :usb_accessInput, :employee_id_from_dropdown_Input);

-- Trainings
SELECT * FROM Trainings; -- select all Trainings

-- add a new training
INSERT INTO Trainings (title, duration_in_min, required_status)
VALUES (:titleInput, :duration_in_minInput, :required_statusInput);

DELETE FROM Trainings where training_id = :training_idInput -- This will cascade in the M:M relationship

-- TrainingDetails
SELECT * FROM TrainingDetails; -- select all TrainingDetails

INSERT INTO TrainingDetails (employee_id, training_id, completion_date, pass_or_fail)
VALUES (:employee_idInput, :training_idInput, :completion_dateInput, :pass_or_failInput)

DELETE FROM TrainingDetails WHERE training_id = :training_idInput

-- Passwords
SELECT * FROM Passwords; -- select all Passwords

-- add a new password
INSERT INTO Passwords (title, password, req_change, employee_id)
VALUES (:titleInput, :passwordInput, :req_changeInput, :employee_idInput)
