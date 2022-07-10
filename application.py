import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, contact_info, profile_page_info, error, majors, full_name, major_name

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///majormatch.db")

# List of graduation class years
class_years = ["2021", "2022", "2023", "2024", "2025"]

# List of Yale residential colleges
colleges = ["Benjamin Franklin", "Berkeley", "Branford", "Davenport", "Ezra Stiles", "Grace Hopper", "Jonathan Edwards", "Morse", "Pauli Murray", "Pierson", "Saybrook", "Silliman", "Timothy Dwight", "Trumbull"]

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET"])
def home():
    # Homepage
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    # Store user's data in variables
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    email = request.form.get("email")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    phone = request.form.get("phone")
    college = request.form.get("college")
    class_year = request.form.get("class")
    major = request.form.get("major")

    # Method is via POST
    if request.method == "POST":

        # Checking if everything that is required was inputted by the user
        if not firstName:
            return error("Enter first name", 403)
        elif not lastName:
            return error("Enter last name", 403)
        elif not email:
            return error("Enter email", 403)
        elif not password:
            return error("Enter password", 403)
        elif not confirmation:
            return error("Enter password confirmation", 403)
        elif not college:
            return error("Enter college", 403)
        elif not class_year:
            return error("Enter class year", 403)
        elif not major:
            return error("Enter major", 403)


        # Passwords don't match
        if password != confirmation:
            return error("Passwords don't match", 403)

        # Check that a Yale email was inputted
        email_split = email.split("@")
        yale_split = email_split[1].split(".")
        if yale_split[0].lower() != "yale":
            return error("Enter a valid Yale email address", 403)

        # Check if email already exists in database
        session = db.execute("SELECT id FROM users WHERE email = :email", email=email)

        # If a username already exists return an error message
        if session:
            return error("Email already exists", 403)

        # Hash password
        hash_password = generate_password_hash(password)

        # Call function to obtain full name of student as one string
        fullname = full_name(firstName, lastName)

        # Call function to obtain the major's name
        majorname = major_name(major)

        # Insert new info into users
        user = db.execute("INSERT INTO users (lastName, firstName, email, phone, college, class, major, password, fullName, majorsymb) VALUES(:l, :f, :e, :p, :c, :y, :m, :h, :full, :sym)", l=lastName, f=firstName, e=email, p=phone, c=college, y=class_year, m=majorname, h=hash_password, full=fullname, sym=major)

        # Redirect user to login page
        return redirect("/login")

    # If method via GET
    else:
        # Obtain all majors from function to pass into webpage
        all_majors = majors()
        return render_template("register.html", majors=all_majors, years=class_years, colleges=colleges)


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # Store user information in variables
    email = request.form.get("email")
    password = request.form.get("password")

    # If method via POST
    if request.method == "POST":

        # Check for email submission
        if not email:
            return error("Please enter your email")

        # Check for password submission
        elif not password:
            return error("Enter password")

        # Query database for email
        check = db.execute("SELECT * FROM users WHERE email = :e", e=email)

        # Ensure username exists and password is correct
        if len(check) != 1 or not check_password_hash(check[0]["password"], password):
            return error("Incorrect username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = check[0]["id"]

        # Redirect user to their profile page
        return redirect("/profile")

    # If method via GET
    else:
        return render_template("login.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    # Obtain student's profile page info
    profile = profile_page_info(session.get("user_id"))

    # Obtain student's contact info
    contact = contact_info(session.get("user_id"))

    # Get students's first name to pass into webpage
    name = db.execute("SELECT firstName FROM users WHERE id = :ID", ID=session.get("user_id"))
    # Store name from query in a variable
    name = name[0]["firstName"]

    # Pass student information onto webpage
    return render_template("profilepage.html", profile=profile, contact=contact, name=name)

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        allmajors = majors()
        return render_template("edit.html", majors=allmajors, years=class_years, colleges=colleges)

    else:
        email = request.form.get("email")
        password = request.form.get("password")
        phone = request.form.get("phone")
        college = request.form.get("college")
        class_year = request.form.get("class")
        major = request.form.get("major")

        if email:
            db.execute("UPDATE users SET email = :e WHERE id = :ID", e=email, ID=session.get("user_id"))

        if password:
            hash_password = generate_password_hash(password)
            db.execute("UPDATE users SET password = :p WHERE id = :ID", p=hash_password, ID=session.get("user_id"))

        if phone:
            db.execute("UPDATE users SET phone = :p WHERE id = :ID", p=phone, ID=session.get("user_id"))

        if college:
            db.execute("UPDATE users SET college = :p WHERE id = :ID", p=college, ID=session.get("user_id"))

        if class_year:
            db.execute("UPDATE users SET class = :p WHERE id = :ID", p=class_year, ID=session.get("user_id"))

        if major:
            majorname = major_name(major)
            db.execute("UPDATE users SET major = :p, majorsymb = :s WHERE id = :ID", p=majorname, s=major, ID=session.get("user_id"))

        return redirect("/profile")

@app.route("/browse", methods=["GET", "POST"])
@login_required
def browse():

    # Store student's major choice in variable (as the major's abbreviation)
    major = request.form.get("major")

    # Method via POST
    if request.method == "POST":

        # Query all students that are pursuing that major except for the own student
        matches = db.execute("SELECT * FROM users WHERE majorsymb = :m EXCEPT SELECT * FROM users WHERE id = :ID", m=major, ID=session.get("user_id"))

        # Check if there are any such matches
        if matches:

            # Obtain major name from calling function
            majorname_ = major_name(major)
            # Open webpage and pass information to it
            return render_template("matched.html", matches=matches, major=majorname_)

        # If no matches are found return error message
        else:
            return error("We found no matches!", "Try again later!")

    # If method via GET
    else:
        # Pass all majors to webpage for student to select major they want to match with
        majors_ = majors()
        return render_template("find.html", majors=majors_)



@app.route("/statement")
def statement():
    # Open page with our platform's mission statement
    return render_template("statement.html")


@app.route("/logout")
def logout():
    # Clear current user's session
    session.clear()
    # Redirect user to homepage
    return redirect("/")
