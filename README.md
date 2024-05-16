# Rulerise Intern Developer Interview Task

This project is an Intern Developer Interview Task for Rulerise, completed by Simo Hakim for the Software Developer Intern Position. The project was developed using Python and Django.

## Project Overview

The objective of this project is to develop a robust API and design for an Employee Management System. The system allows CRUD (Create, Read, Update, and Delete) operations on employee records, role assignment, searching, and status updates. The API documentation is generated using `drf-yasg`.

## Requirements

### Employee CRUD Operations
- Endpoints to perform CRUD operations on employee records.
- Ensure a well-structured payload for creating and updating employees.

### Role Assignment
- Endpoint to allow admins to assign roles to employees.
- Valid roles: [manager, developer, designer, scrum master].

### Search Functionality
- Endpoints to find employees by name and ID.

### Admin Dashboard
- Endpoints to:
  - Retrieve total employees.
  - Retrieve total available roles.
  - Create and delete job roles.

### Status Updates
- Endpoint allowing admins to update the status of an employee (employed or fired).

### Data Consistency
- Ensure that the job role is populated along with other employee information when fetching employee details.

## Technologies Used

- **Python**: Programming language.
- **Django**: Web framework.
- **SQLite**: Database.
- **Django REST Framework**: For building RESTful APIs.
- **drf-yasg**: For generating API documentation.

## How to Run

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Start the server**:
   ```bash
   python manage.py runserver
   ```

4. **Access the API documentation**:
   - Swagger UI: `http://127.0.0.1:8000/swagger/`
   - ReDoc: `http://127.0.0.1:8000/redoc/`

5. **Access the Admin dashboard documentation**:
   - Admin: `http://127.0.0.1:8000/admin/`
    User set by default to simo and password to 1234.