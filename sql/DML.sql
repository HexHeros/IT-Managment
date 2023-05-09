-- Employees
SELECT * FROM Employees; -- select all Employees

SELECT Employees.first_name, Employees.last_name, Roles.title -- Gives a list of software engineers that are active 
FROM Employees
INNER JOIN Roles
ON Roles.role_id = Employees.role_id
WHERE Roles.role_id = 1 and Employees.active = True;

INSERT INTO Employees(first_name, last_name, email, dept_id, active, hire_date, role_id)
VALUES  (:first_nameInput, :last_nameInput, :emailInput, :dept_idInput, :activeInput, :hire_dateInput, :role_id_from_the_dropdown_Input);

DELETE FROM Employees WHERE employee_id = :employee_id_selected_from_employees_page; -- delete selected employee

UPDATE Employees SET first_name = :first_nameInput, last_name= :last_nameInput, email = :emailInput, dept_id= :dept_idInput WHERE id= :employee_ID_from_the_update_form;

-- Departments
SELECT * FROM Departments; -- select all Departments

INSERT INTO Departments (dept_name, manager_employee_id)
VALUES (:dept_nameInput, :manager_employee_id_from_dropdown_Input);

-- Roles
SELECT * FROM Roles; -- select all Roles

INSERT INTO Roles (title, access_level)
VALUES (:titleInput, :access_levelInput);

-- Devices
SELECT * FROM Devices; -- selelct all Devices

INSERT INTO Devices (device_name, type, access_level, usb_access, employee_id)
VALUES (:device_nameInput, :typeInput, :access_levelInput, :usb_accessInput, :employee_id_from_dropdown_Input);

-- Trainings
SELECT * FROM Trainings; -- select all Trainings

INSERT INTO Trainings (title, duration_in_min, required_status)
VALUES (:titleInput, :duration_in_minInput, :required_statusInput);

-- TrainingDetails
SELECT * FROM TrainingDetails; -- select all TrainingDetails

INSERT INTO TrainingDetails (employee_id, training_id, completion_date, pass_or_fail)
VALUES (:employee_idInput, :training_idInput, :completion_dateInput, :pass_or_failInput)

-- Passwords
SELECT * FROM Passwords; -- select all Passwords

INSERT INTO Passwords (title, password, req_change, employee_id)
VALUES (:titleInput, :passwordInput, :req_changeInput, :employee_idInput)
