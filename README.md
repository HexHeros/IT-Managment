# app.py citations

### The app.py file is all based on the CS 340 starter code, with the exception of added route handlers and join queries

Date: 5/25/2023

Based/copied from:

Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app

### In the app.py file under the Employees and edit_employee route handlers, this code was interpreted/copied from w3schools website for LEFT JOIN and aliases
```
SELECT e.employee_id, e.first_name, e.last_name, e.email, d.dept_name, r.title, e.active, e.hire_date 
FROM Employees e 
LEFT JOIN Departments d ON e.dept_id = d.dept_id 
LEFT JOIN Roles r ON e.role_id = r.role_id;
```

Date: 6/5/2023

Adapted/copied from:

Source URL:https://www.w3schools.com/sql/sql_join_left.asp and https://www.w3schools.com/sql/sql_alias.asp

---

### In the app.py file under the departments and edit_departments route handlers, this code was interpreted/copied from w3schools website for LEFT JOIN and aliases
```
SELECT d.dept_id, d.dept_name, e.first_name, e.last_name 
FROM Departments d 
LEFT JOIN Employees e 
ON d.manager_employee_id = e.employee_id;
```

Date: 6/5/2023

Adapted/copied from:

Source URL:https://www.w3schools.com/sql/sql_join_left.asp  and  https://www.w3schools.com/sql/sql_alias.asp

---

### In the app.py file under the devices route handler, this code was interpreted/copied from w3schools website for LEFT JOIN and aliases
```
SELECT d.device_name, d.type, d.access_level, d.usb_access, e.first_name, e.last_name 
FROM Devices d 
LEFT JOIN Employees e 
ON d.employee_id = e.employee_id;"
```

Date: 6/5/2023

Adapted/copied from:

Source URL:https://www.w3schools.com/sql/sql_join_left.asp  and  https://www.w3schools.com/sql/sql_alias.asp

---


# Templates/CSS citations

```
 #   The html files use for loops to grab current information in the database
 #   Date: 6/5/23
 #   Incorporated from:
 #   Source URL: https://stackoverflow.com/questions/45877080/how-to-create-dropdown-menu-from-python-list-using-flask-and-html
```
```
 #   edit_department.html and departments.html uses if else to set a default value of NULL when user selects None from dropdown
 #   Date: 5/30/2023
 #   Incorporated from:
 #   Source URL: https://itecnote.com/tecnote/jinja2-template-variable-if-none-object-set-a-default-value/
```
```
 #   edit_role.html uses a conditional to prefill selected information that is being edited
 #   Date: 5/30/2023
 #   Incorporated/copied from:
 #   Source URL: https://stackoverflow.com/questions/73732603/bringing-select-option-values-to-select-option
```
```
#  These template files use these pre-made icons 
#  Date: 5/30/2023
#  Copied from:
#  Source URL: https://www.w3schools.com/howto/howto_css_icon_buttons.asp
```
```
#  These template files use these pre-made icons 
#  Date: 5/30/2023
#  Copied from:
#  Source URL: https://www.w3schools.com/icons/fontawesome_icons_directional.asp
```
```
#  These template files used this style to add icons to each page
#  Date: 5/30/2023
#  Based/copied from:
#  Source URL: https://stackoverflow.com/questions/54087985/i-cant-get-my-font-awesome-icons-to-show-up-tried-importing-css-with-multiple
```
```
#  These template files uses some html/css from bootstrap for the forms
#  Date: 5/30/2023
#  Based off:
#  Source URL: https://epicbootstrap.com/snippets/registration
```
```
#   edit_employee.html uses a for loop to grab current departments and roles in the database, and pulls what is currently in each field that needs to be edited
#   Date: 6/5/23
#   Incorporated/based off:
#   Source URL: https://stackoverflow.com/questions/74016925/how-to-set-default-selection-in-flask-dropdown-menu-based-on-users-previous-cho
```
```
#  new_employee.html uses a for loop to grab current departments and roles in the database
#   Date: 6/5/23
#   Incorporated from:
#   Source URL: https://stackoverflow.com/questions/45877080/how-to-create-dropdown-menu-from-python-list-using-flask-and-html
```
```
# CSS uses pre-made buttons, forms, and icons
# Date: 5/30/2023
# Copied from:
# Source URL: https://getcssscan.com/css-buttons-examples
# and https://www.w3schools.com/howto/howto_css_icon_buttons.asp
```
