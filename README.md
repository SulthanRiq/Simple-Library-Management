# Simple Library Management
#### Video Demo: https://youtu.be/ZG30vHBrmJA
#### Description: 

This project is the **Final Project** for the CS50x course, developed using the **Flask** framework. It is a simple **Library Management System** web application that allows two types of users: **students** and **administrators (admin)** to interact with the system for digital book borrowing and returning.

Students can log in, borrow books, view their borrowing history, and manage their active loans. Administrators can monitor all borrowing activities, view details of each transaction, and confirm when a book has been returned.

The system uses **SQLite** as its main database, **SQLAlchemy** as the ORM, and **Bootstrap** for the user interface. The project was built to practice skills in **web application development, authentication, database management, Flask routing, and role-based access control**.

---

## Key Features

### Student Features
1. **Registration and Login**
   - Students can create accounts with a username, student number, and password.
   - Passwords are securely stored using hashing.

2. **Borrow Books**
   - Students can borrow books by filling out a form with title, author, borrow date, and return date.
   - Input validation ensures that incomplete forms will not be accepted.

3. **Borrowing History**
   - Students can view all their past and current borrowing records.
   - Displays book title, author, borrow date, and return date.

4. **Logout**
   - Ends the current session and logs the student out securely.

### Admin Features
1. **Admin Login**
   - Admins log in with predefined credentials (hardcoded in this version).
   - Redirects to the admin dashboard after login.

2. **Borrowing Dashboard**
   - Admins can see a list of all borrowings, including student username, book title, author, borrow date, and return date.

3. **Confirm Book Return**
   - Admins can mark books as **Returned** using an action button.
   - A Bootstrap modal appears to confirm the return before updating the status.

4. **Access Control**
   - Admin routes are protected and only accessible to logged-in admins.

---

## Technologies Used

- **Backend Framework**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, Bootstrap
- **Template Engine**: Jinja2 (Flask built-in)
- **Security**: Werkzeug password hashing, session-based authentication
- **Development Tools**:
  - Python Virtual Environment (`venv`)
  - Git for version control

---


---

## Installation and Setup

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd CS50x\ Final\ Project

2. **Create Virtual Environment**
    - python -m venv venv
    - source venv/bin/activate   # macOS/Linux
    - venv\Scripts\activate      # Windows

3. **Install Dependencies**
    - pip install -r requirements.txt
    - If requirements.txt is missing, install the core dependencies manually: Flask, SQLAlchemy, Werkzeug

4. **Initialize Database**
    - The project already includes library.db, but you can recreate it with:  
    from database import Base, engine  
    Base.metadata.create_all(engine)

5. **Run the Application**
    - flask run

6. **Access the Application**
    - Student: http://localhost:5000
    - Admin: http://localhost:5000/admin_index

## Application Workflow

1. As a Student
    - Register or log in with your student account.
    - Access the homepage (/) to view currently borrowed books.
    - Use the Borrow menu to borrow a new book by filling in the form.
    - View your borrowing history in the History section.
    - Logout to end your session.

2. As an Admin
    - Log in with admin credentials (username: admin, password: 12345678 in this version).
    - Access the Admin Dashboard.
    - Monitor all student borrowings, with details of each transaction.
    - Use the Return button to mark a book as returned → confirmation modal → status updated to Returned.

## Security
1. Student passwords are stored securely using Werkzeug hashing.
2. Session cookies ensure authentication persistence.
3. Role-based access control ensures students cannot access admin pages.
4. Admin session is tracked with a is_admin flag in the session.

## Future Improvements
1. Book Catalog Management
    - Add a books table to store a complete catalog of available books.
    - Allow admin to add, edit, or delete books.

2. Admin Registration
    - Replace hardcoded credentials with a proper admin registration system.

3. Notifications & Reminders
    - Send email when the return deadline is near.

4. Export Data
    - Allow admins to export borrowing data in CSV or PDF format.

5. Improved UI/UX
    - Add AJAX or Fetch API for smoother, real-time updates without full page reloads.

## Conclusion
This project is a practical implementation of CRUD operations (Create, Read, Update, Delete), user authentication, and role-based access control within a web application. Using Flask as the backend, SQLite as the database, and Bootstrap for styling, the application is lightweight, easy to run, and extendable.

Even though it is simple, the project already includes essential aspects of modern web development: authentication, relational database design, template rendering, secure sessions, and user-friendly interfaces. It serves as a strong foundation for building more advanced library or resource management systems in the future.


