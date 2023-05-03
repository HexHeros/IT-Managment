SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0


CREATE OR REPLACE TABLE Employees (
    employee_id int not null auto_increment,
    first_name nvarchar(255) not null,
    last_name nvarchar(255) not null,
    email nvarchar(255) not null,
    department_id int not null,
    active bit not null,
    hire_date date,
    role_id int,
    primary key(employee_id),
    foreign key(role_id) references Roles(role_id),
    foreign key(department_id) references Departments(department_id),
    on delete set null  -- if departemnt or role are deleted we dont necessarily want to delete the employee
);

INSERT INTO Employees(employee_id, first_name, last_name, email, department, active, hire_date, role)
VALUES 
(1, ‘Devri’, ‘Anderson’, ‘da@coder.com’, 1, 1, ‘2023-1-1’, 1),
(2, ‘Jacob’, ‘Ogle’, ‘jo@coder.com’, 3, 1,’2023-1-2’,  2),
(3, ‘Michael’, ‘Scott’, ‘prisonmike@coder.com’, 2, 1, ‘2023-04-29’, 9);


CREATE OR REPLACE TABLE Devices(
    device_id int not null auto_increment,
    device_name nvarchar(255) not null,
    type nvarchar(255),
    access_level int not null,
    usb_access int not null,
    primary key(device_id),
    employee_id int,
    foreign key(employee_id) references Employees(employee_id),
    on delete set null -- if employee is deleted we may want to keep device
);

INSERT INTO Devices(device_id, device_name, type, access_level, usb_access)
VALUES
(1, ‘Macbook Pro’, ‘Laptop’, 3, 0, 3),
(2, ‘iPhone 14’, ’Mobile’, 1, 1, 2),
(3, ‘iMac’, ‘Desktop’, 1, 1, 1);

CREATE OR REPLACE TABLE Departments(
    dept_id int auto_increment,
    name - nvarchar(255),
    manager - emp_id,
    primary key(dept_id),
    foreign key(manager) references Employees(employee_id),
    on delete set null -- if employee is deleted we mw want to keep the dept
);

INSERT INTO Departments(dept_id, name, manager)
VALUES
(1, ‘Software Engineering’, 1),
(2, ‘Management’, 3),
(3, ‘Data Analytics’, 2);

CREATE OR REPLACE TABLE Roles(
    role_id int auto_increment,
    title nvarchar(255),
    access_level int ,
    primary key(role_id)
);

INSERT INTO Roles(role_id, title, access_level)
VALUES
(1, ‘Software Engineer’, 1),
(2, ‘Data Engineer’, 1),
(3, ‘Intern’, 10)
(4, ‘CEO’, 1),
(5, ‘CTO’, 1),
(6, ‘CFO’, 1)
(7, ‘IT’, 1),
(8, ‘Assistant to General Manager’, 6),
(9, ‘General Manager’, 3);

CREATE OR REPLACE TABLE Trainings(
    training_id int auto_increment,
    title nvarchar(255),
    duration_in_min int,
    required_status bit not null,
    primary key(training_id),
);

INSERT INTO Trainings(training_id, title, duration_in_min, required_status)
VALUES
(1, ‘SQL Certification’, 120, 1),
(2, ‘Reverse Running in Red Rock’, 10, 0),
(3, ‘Don’t get hacked 101’, 60, 0);

CREATE OR REPLACE TABLE Passwords(
    password_id int auto_increment,
    pass nvarchar(255),
    req_change bit not null,
    primary key(password_id),
    foreign key(employee_id) references Employees(employee_id),
    cascade on delete -- if employee is deleted no reason to keep password
);

INSERT INTO Passwords(password_id, title, password, req_change, employee_id)
VALUES
(1, ‘abc123*!’, 0, 1),
(2, ‘password’, 0, 2),
(3, ‘DunderMifflin1’, 1, 0);


CREATE OR REPLACE TABLE TrainingDetails(
    training_details_id int auto_increment,
    training_id int,
    completion_date date,
    pass_or_fail bit not null,
    foreign key(employee_id) references Employees(employee_id),
    foreign key(training_id) references Trainings(training_id),
    cascade on delete -- if the employee or training is deleted there is no reason to keep training record
);

INSERT INTO TrainingDetails(training_id, title, duration_in_min, required_status)
VALUES
(1, 2, 1, ‘2023-1-5’, 1),
(2, 3, 3, ‘2023-5-1’, 1),
(3, 1, 2, ‘2023-6-1’, 1);

SET FOREIGN_KEY_CHECKS=1;
COMMIT;





