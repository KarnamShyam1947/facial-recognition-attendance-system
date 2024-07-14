from unittest import result
from flask import Flask, flash, redirect, render_template, request, session, url_for
# from utils.query import get_result
from utils.insert import insert
from utils.admin import add_faculty, add_student, login

app = Flask(__name__)
app.secret_key = "this-is-secret"

# @app.route("/insert", methods=['GET', 'POST'])
# def insert_user():
#     if request.method == 'POST':
#         file = request.files.get("file", None)
#         name = request.form.get("name", None)
        
#         if not file or not name:
#             return render_template("insert.html", msg = "error : all fields reqired")

#         else:
#             file_path = "faces/temp.jpg"
#             file.save(file_path)
            
#             flag = insert(file_path, name)

#             if flag:
#                 return render_template("insert.html", msg = "success : face added")

#             else:
#                 return render_template("insert.html", msg = "error : face not detected")
        
#     return render_template("insert.html", msg = "")

# @app.route("/result", methods=['GET', 'POST'])
# def result():
#     if request.method == 'POST':
#         file = request.files.get("file", None)
        
#         if not file:
#            return render_template("result.html", msg = "error : select a file") 
       
#         else:
#             file_path = "faces/web.jpg"
#             file.save(file_path)
            
#             result = get_result(file_path)
            
#             return render_template("result.html", msg = result, r = True)
    
#     return render_template("result.html", msg = "")

@app.route("/login", methods = ['GET', 'POST'])
def login_user():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        result = login(email, password)

        if not result:
            flash("Invalid user details", "danger")
            return render_template("login.html")
        
        else:
            session['current_user'] = result
            return "Hello, World"


    return render_template("login.html")

@app.route("/add-faculty", methods = ['GET', 'POST'])
def add_faculty_render():
    if 'current_user' not in session:
        flash("You need to login to access this page", "danger")
        return redirect(url_for("login_user"))
    
    if session['current_user']['role'] != 'ADMIN':
        flash("403 : unauthenticated user")
        return redirect(url_for("login_user"))

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        result = add_faculty(name, email, password)

        if result:
            flash("Faculty added successfully", "success")
        
        else:
            flash("Email already register", "danger")

        return redirect(url_for("add_faculty_render"))

    return render_template("admin/add-faculty.html")

@app.route("/add-student", methods = ['GET', 'POST'])
def add_student_render():
    if 'current_user' not in session:
        flash("You need to login to access this page", "danger")
        return redirect(url_for("login_user"))
    
    if session['current_user']['role'] != 'ADMIN':
        flash("403 : unauthenticated user")
        return redirect(url_for("login_user"))
    
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        file = request.files.get("image")
        file_path = "temp.png"

        result = add_student(name, email, password)

        if result:
            file.save(file_path)
            insert(file_path, name)
            flash("Student added successfully", "success")
        
        else:
            flash("Email already register", "danger")

        return redirect(url_for("add_student_render"))

    return render_template("admin/add-student.html")

@app.route("/logout")
def logout():
    session.pop("current_user", None)
    return redirect(url_for("login_user"))

if __name__ == "__main__":
    app.run(debug=True)
