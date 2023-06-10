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
    active varchar(3) not null,
    hire_date date,
    role_id int not null,
    primary key(employee_id)
);

--
-- Dumping data for table `Employees`
--

INSERT INTO Employees(first_name, last_name, email, dept_id, active, hire_date, role_id)
VALUES 
('Devri', 'Anderson', 'da@coder.com', 1, 'Yes', '2023-01-01', 1),
('Jacob', 'Ogle', 'jo@coder.com', 3, 'Yes', '2023-01-02',  2),
('Michael', 'Scott', 'prisonmike@coder.com', 2, 'Yes', '2023-04-29', 9);

--
-- Table structure for table `Devices`
--

CREATE OR REPLACE TABLE Devices(
    device_id int not null auto_increment,
    device_name varchar(255) not null,
    type varchar(255),
    access_level int not null,
    usb_access varchar(3) not null,
    primary key(device_id),
    employee_id int,
    foreign key(employee_id) references Employees(employee_id) on delete set null -- if employee is deleted we may want to keep device
);

--
-- Dumping data for table `Devices`
--

INSERT INTO Devices(device_name, type, access_level, usb_access, employee_id)
VALUES
('Macbook Pro', 'Laptop', 3, 'No', 3),
('iPhone 14', 'Mobile', 1, 'Yes', 2),
('iMac', 'Desktop', 1, 'Yes', 1);

--
-- Table structure for table `Departments`
--

CREATE OR REPLACE TABLE Departments(
    dept_id int not null auto_increment,
    dept_name nvarchar(255),
    manager_employee_id int,
    primary key(dept_id),
    foreign key(manager_employee_id) references Employees(employee_id) on delete set null -- if employee is deleted we mw want to keep the dept
);

--
-- Dumping data for table `Departments`
--

INSERT INTO Departments(dept_name, manager_employee_id)
VALUES
('Software Engineering', 1),
('Management', 3),
('Data Analytics', 2);

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

INSERT INTO Roles(title, access_level)
VALUES
('Software Engineer', 1),
('Data Engineer', 1),
('Intern', 10),
('CEO', 1),
('CTO', 1),
('CFO', 1),
('IT', 1),
('Assistant to General Manager', 6),
('General Manager', 3);

--
-- Table structure for table `Trainings`
--

CREATE OR REPLACE TABLE Trainings(
    training_id int not null auto_increment,
    title nvarchar(255),
    duration_in_min int,
    required_status varchar(3) not null,
    primary key(training_id)
);

--
-- Dumping data for table `Trainings`
--

INSERT INTO Trainings(title, duration_in_min, required_status)
VALUES
('SQL Certification', 120, 'Yes'),
('Reverse Running in Red Rock', 10, 'No'),
('Don’t Get Hacked 101', 60, 'No');

--
-- Table structure for table `Passwords`
--

CREATE OR REPLACE TABLE Passwords(
    password_id int not null auto_increment,
    password varchar(255) not null,
    req_change varchar(3) not null,
    employee_id int,
    primary key(password_id),
    foreign key(employee_id) references Employees(employee_id) on delete cascade -- if employee is deleted no reason to keep password
);

--
-- Dumping data for table `Passwords`
--

INSERT INTO Passwords(password, req_change, employee_id)
VALUES
('abc123*!', 'No', 1),
('password', 'No', 2),
('DunderMifflin1', 'Yes', 3);

--
-- Table structure for table `TrainingDetails`
--

CREATE OR REPLACE TABLE TrainingDetails(
    training_details_id int not null auto_increment,
    employee_id int,
    training_id int,
    completion_date date not null,
    pass_or_fail varchar(4) not null,
    primary key(training_details_id),
    foreign key(employee_id) references Employees(employee_id) on delete cascade,
    foreign key(training_id) references Trainings(training_id) on delete cascade -- if the employee is deleted there is no reason to keep training record
);

--
-- Dumping data for table `TrainingDetails`
--

INSERT INTO TrainingDetails(employee_id, training_id, completion_date, pass_or_fail)
VALUES
(2, 1, '2023-05-01', 'Pass'),
(3, 3, '2023-01-05', 'Pass'),
(1, 2, '2023-06-01', 'Pass');

SET FOREIGN_KEY_CHECKS=1;
COMMIT;
