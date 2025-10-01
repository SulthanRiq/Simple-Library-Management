from flask import Flask, render_template, session, redirect, request, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy import select, insert, update
from datetime import datetime

from helpers import login_required, admin_required
from models import Borrow, Students
from database import db_session, Base, engine

import os, time

UPLOAD_FOLDER = os.path.join('static', 'uploads')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = "super secret key"

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if __name__ == "__main__":
    app.debug(True)
    app.run()

Base.metadata.create_all(bind=engine)


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
@login_required
def index():

    books = db_session.query(Borrow.borrow_id ,Borrow.book_title, Borrow.book_writer, Borrow.borrow_date, Borrow.return_date, Borrow.status, Borrow.image_path).filter(
        Borrow.student_id == session["user_id"]
    ).all()

    books_info = []

    for book in books:
        books_info.append(book)

    return render_template("index.html", books=books, books_info=books_info)


@app.route("/admin_index", methods=["GET", "POST"])
@admin_required
def admin_index():

    books = db_session.query(
        Borrow.borrow_id,
        Borrow.book_title,
        Borrow.book_writer,
        Borrow.borrow_date,
        Borrow.return_date,
        Borrow.status,
        Students.username.label("student_name")
    ).join(Students, Borrow.student_id == Students.id).all()


    return render_template("admin/admin_index.html", books=books)


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("errors/error.html")
        
        if username == "admin" and password == "12345678":
            session["is_admin"] = True
            return redirect("/admin_index")
        
        
        rows = db_session.query(Students).filter_by(username=username).first()

        # if len(rows) != 1 or not check_password_hash(
        #     rows[0].hash, request.form.get("password")
        # ):
        #     return render_template("errors/error.html")

        if rows is None or not check_password_hash(rows.password, password):
            return render_template("errors/error.html")

        session["user_id"] = rows.id
        session["is_admin"] = False    

        return redirect("/")
    
    else:
        return render_template("students/student_login.html")



@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():

    username = request.form.get("username")
    student_number = request.form.get("student_number")
    password = request.form.get("password")
    confirm_password = request.form.get("confirmation")

    if request.method == "POST":
        if username == "":
            return render_template("errors/error.html")
        elif student_number == "":
            return render_template("errors/error.html")
        elif password == "":
            return render_template("errors/error.html")
        elif confirm_password == "":
            return render_template("errors/error.html")
        elif password != confirm_password:
            return render_template("errors/error.html")
        else:
            try:
                hash = generate_password_hash(password)
                new_user = Students(username=username, student_number=student_number, password=hash)

                db_session.add(new_user)
                db_session.commit()
                db_session.refresh(new_user)

                # insert(Students).values(username=username, student_number=student_number, password=hash)
                # new_user = select(Students.id).where(Students.username == username)
            except Exception as e:
                print("Error: ", e)
                db_session.rollback()
                return render_template("errors/error.html")
            else:
                session["user_id"] = new_user.id
                return redirect("/")

    if request.method == "GET":
        return render_template("students/student_register.html")

@app.route("/borrow", methods=["GET", "POST"])
@login_required
def borrow():

    book_title = request.form.get("book_title")
    book_writer = request.form.get("book_writer")
    publication_year = request.form.get("publication_year")
    borrow_date_str = request.form.get("borrow_date")
    return_date_str = request.form.get("return_date")
    upload_file = request.files.get("book_image")

    if request.method == "POST":
        if book_title == "":
            return render_template("errors/error.html")
        elif book_writer == "":
            return render_template("errors/error.html")
        elif publication_year == "":
            return render_template("errors/error.html")
        elif not borrow_date_str:
            return render_template("errors/error.html")
        elif not return_date_str:
            return render_template("errors/error.html")
        
        if not upload_file or upload_file.filename == '':
            return "No file selected", 400
        
        if upload_file and allowed_file(upload_file.filename):
            filename = str(int(time.time())) + "_" + secure_filename(upload_file.filename)
            filepath = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
            upload_file.save(filepath)
        
        borrow_date = datetime.strptime(borrow_date_str, "%Y-%m-%d").date()
        return_date = datetime.strptime(return_date_str, "%Y-%m-%d").date()
    
        new_borrow = Borrow(
            student_id=session["user_id"],
            book_title=book_title,
            book_writer=book_writer,
            publication_year=publication_year,
            image_path=filepath,
            borrow_date=borrow_date,
            return_date=return_date,
            status="Borrowed"
        )


        db_session.add(new_borrow)
        db_session.commit()


        flash("The book has been successfully borrowed!")
        return redirect("/")


    if request.method == "GET":
        return render_template("students/borrow_page.html")
    

@app.route("/history")
@login_required
def history():
    
    histories = db_session.query(Borrow.book_title, Borrow.book_writer, Borrow.borrow_date, Borrow.return_date, Borrow.status).filter(
        Borrow.student_id == session["user_id"]
    ).all()

    histories_info = []

    for history in histories:
        histories_info.append(history)

    return render_template("students/borrow_histories.html", histories=histories, histories_info=histories_info)



@app.route("/return_book", methods=["GET", "POST"])
@admin_required
def return_book():
    borrow_id = request.form.get("borrow_id")

    if not borrow_id:
        flash("Invalid request!", "danger")
        return redirect("/admin_index")
    
    borrow_record = db_session.query(Borrow).filter_by(borrow_id=borrow_id).first()

    if not borrow_record:
        flash("Borrow record not found!", "danger")
        return redirect("/admin_index")
    

    borrow_record.status = "Returned"
    db_session.commit()

    flash("The book has been successfully returned!", "success")
    return redirect("/admin_index")