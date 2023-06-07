---------------------------------------------- Employees

-- Displays all employees active/inactive - uses LEFT JOIN - displays department name and role title instead of ID
SELECT e.employee_id, e.first_name, e.last_name, e.email, d.dept_name, r.title, e.active, e.hire_date 
FROM Employees e 
LEFT JOIN Departments d 
ON e.dept_id = d.dept_id 
LEFT JOIN Roles r 
ON e.role_id = r.role_id;

----------------------------------------------------- new_employee

-- add a new employee - : represents the users input
INSERT INTO Employees(first_name, last_name, email, dept_id, active, hire_date, role_id)
VALUES  (:first_nameInput, :last_nameInput, :emailInput, :dept_idInput, :activeInput, :hire_dateInput, :role_id_from_the_dropdown_Input);

-- 
SELECT dept_id, dept_name FROM Departments;

--
SELECT role_id, title FROM Roles;

------------------------------------------------ edit_employee

-- update a Employees's data based on submission of the Update Employee form : represents the users input
UPDATE Employees SET first_name = :first_nameInput, last_name= :last_nameInput, email = :emailInput, dept_id= :dept_idInput, active= :activeInput, hire_date= hire_dateInput, role_id= role_idInput ADD
WHERE id= :employee_ID_from_the_update_form;

-- uses LEFT JOIN - get dept_name and title instead of their IDs - retrieves all employees even if they aren't assigned a dept/role
SELECT e.employee_id, e.first_name, e.last_name, e.email, e.dept_id, e.active, e.hire_date, r.role_id, r.title, d.dept_id, d.dept_name 
FROM Employees e 
LEFT JOIN Departments d 
ON e.dept_id = d.dept_id 
LEFT JOIN Roles r 
ON e.role_id = r.role_id 
WHERE employee_id= :employee_id_selected_for_edit;

SELECT dept_id, dept_name FROM Departments;

SELECT role_id, title FROM Roles;

---------------------------------------------------- delete_people

-- delete selected employee
DELETE FROM Employees WHERE employee_id = :employee_id_selected_from_employees_page; 

----------------------------------------------------- Departments

--  Retrieve departments using a left join to show manager's name instead of ID 
SELECT d.dept_id, d.dept_name, e.first_name, e.last_name
FROM Departments d 
LEFT JOIN Employees e 
ON d.manager_employee_id = e.employee_id; 

----------------------------------------------------- new_department
-- POST - Retrieve the first and last name of the selected manager 
SELECT first_name, last_name FROM Employees WHERE employee_id = :employee_id_selected_from_dropdown;

-- Insert the new department with the retrieved manager_id
INSERT INTO Departments (dept_name, manager_employee_id)
VALUES (:dept_nameInput, :manager_employee_id_from_dropdown_Input);

-- GET - Retrieves all IDs, first and last names of employees
SELECT employee_id, first_name, last_name FROM Employees;

----------------------------------------------------- edit_department

-- update a Department's manager based on the Update form : represents users input
UPDATE Departments SET dept_name = :dept_nameEdit manager_employee_id = :new_emp_id; 

UPDATE Departments SET manager_employee_id = NULL; -- Nullify the current manager ** this has not been added **

-- Retrieve departments using left join to get first and last name instead of ID
-- Ensure all departments are included even if they aren't assigned to an employee
SELECT DISTINCT d.dept_id, d.dept_name, d.manager_employee_id, e.first_name, e.last_name 
FROM Departments d 
LEFT JOIN Employees e 
ON d.manager_employee_id = e.employee_id 
WHERE d.dept_id = {dept_id};

----------------------------------------------------- delete_department

-- delete selected department : represents selected ID
DELETE FROM Departments WHERE dept_id = :id_selected_from_departments

----------------------------------------------------- Devices

-- Retrieve devices using left join to get firs and last name instead of ID
-- ensure all devices are included even if they aren't assigned to an employee
SELECT d.device_id, d.device_name, d.type, d.access_level, d.usb_access, e.first_name, e.last_name 
FROM Devices d 
LEFT JOIN Employees e 
ON d.employee_id = e.employee_id;

----------------------------------------------------- new_device

-- inserts new device based on users input
INSERT INTO Devices (device_name, type, access_level, usb_access, employee_id)
VALUES (:device_nameInput, :typeInput, :access_levelInput, :usb_accessInput, :employee_id_from_dropdown_Input);

-- Retrieve a list of employees for device assignment dropdown
SELECT employee_id, first_name, last_name FROM Employees;

----------------------------------------------------- delete_device

-- delete selected device : represents selected ID
DELETE FROM Devices WHERE device_id = :id_selected_from_devices

----------------------------------------------------- Roles

-- select all Roles
SELECT * FROM Roles; 

-------------------- new_role

-- Insert a new role with the specified title and access level
INSERT INTO Roles (title, access_level)
VALUES (:titleInput, :access_levelInput);

-------------------- edit_role

-- update the title and access level of a role based on ID
UPDATE Roles 
SET title = :titleEdit,  access_level = :access_levelEdit 
WHERE role_id = :id_selected_from_roles

-- retrieve role details for specific role
SELECT * FROM Roles WHERE role_id = :id_selected_from_roles

-- retrieve title 
SELECT DISTINCT title FROM Roles

-------------------- delete_role

-- delete selected role : represents selected ID
DELETE FROM Roles WHERE role_id = :id_selected_from_roles;

----------------------------------------------------- Trainings

-- select all Trainings
SELECT * FROM Trainings; 

-------------------- add a new_train
INSERT INTO Trainings (title, duration_in_min, required_status)
VALUES (:titleInput, :duration_in_minInput, :required_statusInput);

-------------------- delete_training

-- delete selected training : represents selected ID
DELETE FROM Trainings where training_id = :training_idInput -- This will cascade in the M:M relationship

----------------------------------------------------- TrainingDetails

-- select all TrainingDetails
SELECT * FROM TrainingDetails; 

-- retrieve trainings for dropdown
SELECT training_id FROM Trainings;

-- retrieve all employees to assign a training
SELECT * FROM Employees;

-- insert training details for an employee : represents user's input
INSERT INTO TrainingDetails (employee_id, training_id, completion_date, pass_or_fail)
VALUES (:employee_idInput, :training_idInput, :completion_dateInput, :pass_or_failInput)

-------------------- delete_training_log

-- delete selected training details : represents selected ID
DELETE FROM TrainingDetails WHERE training_id = :training_idInput

----------------------------------------------------- Passwords
SELECT * FROM Passwords; -- select all Passwords

-- add a new password : represents user's input
INSERT INTO Passwords (title, password, req_change, employee_id)
VALUES (:titleInput, :passwordInput, :req_changeInput, :employee_idInput)
