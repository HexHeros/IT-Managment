SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

--
-- Table structure for table `Employees`
--

CREATE OR REPLACE TABLE Employees (
    employee_id int not null auto_increment,
    first_name varchar(255) not null,
    last_name varchar(255) not null,
    email varchar(255) not null,
    dept_id int not null,
    active bit not null,
    hire_date date,
    role_id int,
    primary key(employee_id),
    foreign key(role_id) references Roles(role_id),
    foreign key(dept_id) references Departments(dept_id),
    on delete set null  -- if department or role are deleted we dont necessarily want to delete the employee
);

--
-- Dumping data for table `Employees`
--

INSERT INTO Employees(employee_id, first_name, last_name, email, dept_id, active, hire_date, role_id)
VALUES 
(1, ‘Devri’, ‘Anderson’, ‘da@coder.com’, 1, 1, ‘2023-01-01’, 1),
(2, ‘Jacob’, ‘Ogle’, ‘jo@coder.com’, 3, 1,’2023-01-02’,  2),
(3, ‘Michael’, ‘Scott’, ‘prisonmike@coder.com’, 2, 1, ‘2023-04-29’, 9);

--
-- Table structure for table `Devices`
--

CREATE OR REPLACE TABLE Devices(
    device_id int not null auto_increment,
    device_name varchar(255) not null,
    type varchar(255),
    access_level int not null,
    usb_access bit not null,
    primary key(device_id),
    employee_id int,
    foreign key(employee_id) references Employees(employee_id),
    on delete set null -- if employee is deleted we may want to keep device
);

--
-- Dumping data for table `Devices`
--

INSERT INTO Devices(device_id, device_name, type, access_level, usb_access, employee_id)
VALUES
(1, ‘Macbook Pro’, ‘Laptop’, 3, 0, 3),
(2, ‘iPhone 14’, ’Mobile’, 1, 1, 2),
(3, ‘iMac’, ‘Desktop’, 1, 1, 1);

--
-- Table structure for table `Departments`
--

CREATE OR REPLACE TABLE Departments(
    dept_id int not null auto_increment,
    dept_name nvarchar(255),
    manager_employee_id int,
    primary key(dept_id),
    foreign key(manager_employee_id) references Employees(employee_id),
    on delete set null -- if employee is deleted we mw want to keep the dept
);

--
-- Dumping data for table `Departments`
--

INSERT INTO Departments(dept_id, dept_name, manager_employee_id)
VALUES
(1, ‘Software Engineering’, 1),
(2, ‘Management’, 3),
(3, ‘Data Analytics’, 2);

--
-- Table structure for table `Roles`
--

CREATE OR REPLACE TABLE Roles(
    role_id int not null auto_increment,
    title nvarchar(255),
    access_level int,
    primary key(role_id)
);

--
-- Dumping data for table `Roles`
--

INSERT INTO Roles(role_id, title, access_level)
VALUES
(1, ‘Software Engineer’, 1),
(2, ‘Data Engineer’, 1),
(3, ‘Intern’, 10),
(4, ‘CEO’, 1),
(5, ‘CTO’, 1),
(6, ‘CFO’, 1),
(7, ‘IT’, 1),
(8, ‘Assistant to General Manager’, 6),
(9, ‘General Manager’, 3);

--
-- Table structure for table `Trainings`
--

CREATE OR REPLACE TABLE Trainings(
    training_id int not null auto_increment,
    title nvarchar(255),
    duration_in_min int,
    required_status bit not null,
    primary key(training_id),
);

--
-- Dumping data for table `Trainings`
--

INSERT INTO Trainings(training_id, title, duration_in_min, required_status)
VALUES
(1, ‘SQL Certification’, 120, 1),
(2, ‘Reverse Running in Red Rock’, 10, 0),
(3, ‘Don’t get hacked 101’, 60, 0);

--
-- Table structure for table `Passwords`
--

CREATE OR REPLACE TABLE Passwords(
    password_id int not null auto_increment,
    password varchar(255) not null,
    req_change bit not null,
    employee_id int,
    primary key(password_id),
    foreign key(employee_id) references Employees(employee_id),
    on delete cascade -- if employee is deleted no reason to keep password
);

--
-- Dumping data for table `Passwords`
--

INSERT INTO Passwords(password_id, password, req_change, employee_id)
VALUES
(1, ‘abc123*!’, 0, 1),
(2, ‘password’, 0, 2),
(3, ‘DunderMifflin1’, 1, 3);

--
-- Table structure for table `TrainingDetails`
--

CREATE OR REPLACE TABLE TrainingDetails(
    training_details_id int not null auto_increment,
    employee_id int,
    training_id int,
    completion_date date,
    pass_or_fail bit not null,
    foreign key(employee_id) references Employees(employee_id),
    foreign key(training_id) references Trainings(training_id),
    on delete cascade -- if the employee is deleted there is no reason to keep training record
);

--
-- Dumping data for table `TrainingDetails`
--

INSERT INTO TrainingDetails(training_details_id, employee_id, training_id, completion_date, pass_or_fail)
VALUES
(1, 2, 1, ‘2023-05-01’, 1),
(2, 3, 3, ‘2023-01-05’, 1),
(3, 1, 2, ‘2023-06-01’, 1);

SET FOREIGN_KEY_CHECKS=1;
COMMIT;





