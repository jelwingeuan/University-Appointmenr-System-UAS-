from flask import Flask, render_template, request, redirect, url_for,jsonify
from flask import session, flash
from flask_login import LoginManager, UserMixin, login_required, current_user
from db_functions import (
    update_user_info,
    create_appointment,
    get_appointments,
    update_appointment,
    delete_appointment,
)
import sqlite3
import bcrypt
import random
import os

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = "jelwin"
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


class User(UserMixin):
    def __init__(self, id):
        self.id = id


# Function to get database connection
def get_db_connection():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    return con


@login_manager.user_loader
def load_user(id):
    # Load and return a user from the database based on user_id
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (id,))
    user = cur.fetchone()
    con.close()
    if user:
        return User(user["id"])
    else:
        return None


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


# Function for hashed password
def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")


# Route for "sign up"
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        role = request.form.get("role")
        if role == "teacher":
            # If the selected role is "teacher", redirect to the teacher sign-up page
            return redirect("/signupteacher")
        else:
            faculty = request.form.get("faculty")
            username = request.form.get("username")
            email = request.form.get("email")
            phone_number = request.form.get("phone_number")
            password = request.form.get("password")

            if not password:  # Check if password is provided
                return render_template("signup.html", message="Password is required")

            hashed_password = hash_password(password)

            con = get_db_connection()
            cur = con.cursor()

            # Check if email already exists
            cur.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cur.fetchone()

            if user:
                con.close()
                return render_template(
                    "signup.html", message="User with this email already exists"
                )
            else:
                cur.execute(
                    "INSERT INTO users (role, faculty, username, email, phone_number, password) VALUES (?, ?, ?, ?, ?, ?)",
                    (role, faculty, username, email, phone_number, hashed_password),
                )
                con.commit()
                con.close()
                return redirect("/signupflash")
    else:
        return render_template("signup.html")


# Route for signupteacher

# # Route for signupteacjer
# @app.route("/signupteacher", methods=["GET", "POST"])
# def signupteacher():
#     if request.method == "POST":
#         pin_number = request.form.get("pin_number")

#         # Check if the entered PIN number is correct
#         if pin_number != "006942000":
#             return render_template("signinteacher.html", message="Incorrect PIN number")

#         # PIN is correct, proceed with saving teacher details
#         faculty = request.form.get("faculty")
#         username = request.form.get("username")
#         email = request.form.get("email")
#         phone_number = request.form.get("phone_number")
#         password = request.form.get("password")

#         hashed_password = hash_password(password)

#         con = get_db_connection()
#         cur = con.cursor()

#         try:
#             # Check if email already exists
#             cur.execute("SELECT * FROM users WHERE email = ?", (email,))
#             user = cur.fetchone()

#         if user:
#             con.close()
#             return render_template(
#                 "signup.html", message="User with this email already exists"
#             )
#         else:
#             cur.execute(
#                 "INSERT INTO users (role, faculty, username, email, phone_number, password) VALUES (?, ?, ?, ?, ?, ?)",
#                 ("teacher", faculty, username, email, phone_number, hashed_password),
#             )
#             con.commit()
#             con.close()
#             return redirect(
#                 "/signupflash"
#             )  # Redirect to signup flash page upon successful signup
#     else:
#         return render_template("signupteacher.html")


# @app.route("/verify_pin", methods=["POST"])
# def verify_pin():
#     if request.method == "POST":
#         pin = request.form.get("pin_number")  # Update to match the form field name
#         # Verify PIN number
#         if pin == "006942000":  # Replace with your actual PIN
#             # Proceed with saving teacher details
#             return redirect("/signupflash")
#         else:
#             return render_template("signupteacher.html", message="Incorrect PIN number")


# @app.route("/save_teacher_details", methods=["POST"])
# def save_teacher_details():
#     if request.method == "POST":
#         # Extract teacher details from the form
#         role = "teacher"
#         faculty = request.form.get("faculty")
#         username = request.form.get("username")
#         email = request.form.get("email")
#         phone_number = request.form.get("phone_number")
#         password = request.form.get("password")

#         # Hash the password
#         hashed_password = hash_password(password)

#         # Save teacher details to the database
#         con = get_db_connection()
#         cur = con.cursor()
#         cur.execute(
#             "INSERT INTO users (role, faculty, username, email, phone_number, password) VALUES (?, ?, ?, ?, ?, ?)",
#             (role, faculty, username, email, phone_number, hashed_password),
#         )
#         con.commit()
#         con.close()
#         # Redirect to home page
#         return redirect("/")


# Route for "log in"
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email == "admin@example.com" and password == "123":
            session["logged_in"] = True
            return redirect("/admin")
            session["logged_in"] = True
            return redirect("/admin")
        else:
            # If not admin, proceed with regular user login logic
            con = get_db_connection()
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cur.fetchone()

            if user and check_password_hash(user["password"], password):
                # Redirect to the home page upon successful login for regular users
                session["logged_in"] = True
                session["id"] = user[0]
                return redirect("/flash")
                session["logged_in"] = True
                session["id"] = user[0]
                return redirect("/flash")
            else:
                return render_template(
                    "login.html", message="Invalid email or password"
                )
    else:
        return render_template("login.html")


# Route for updating user information
@app.route("/update_user_info", methods=["POST"])   
def update_user():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")
        update_user_info(session["id"], username, email, phone_number)

        return redirect('/profile')



# Route for changing password
@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        # Verify if new password and confirm password match
        if new_password != confirm_password:
            return render_template(
                "profile.html", message="New password and confirm password do not match"
            )
            return render_template(
                "profile.html", message="New password and confirm password do not match"
            )

        # Verify if the current password is correct
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT password FROM users WHERE id = ?", (session["id"],))
        cur.execute("SELECT password FROM users WHERE id = ?", (session["id"],))
        user_data = cur.fetchone()

        if not user_data or not bcrypt.checkpw(
            current_password.encode("utf-8"), user_data["password"].encode("utf-8")
        ):
            return render_template("profile.html", message="Incorrect current password")
        if not user_data or not bcrypt.checkpw(
            current_password.encode("utf-8"), user_data["password"].encode("utf-8")
        ):
            return render_template("profile.html", message="Incorrect current password")

        # Update the password in the database
        hashed_new_password = hash_password(new_password)
        cur.execute(
            "UPDATE users SET password = ? WHERE id = ?",
            (hashed_new_password, session["id"]),
        )
        con.commit()
        con.close()

        # Redirect the user to a success page or profile page
        return redirect("/profile")
    else:
        # Render the profile page with the password change form
        return render_template("profile.html")



# # Function to create a new appointment
# @app.route("/make_appointment", methods=["POST"])
# def make_appointment():
#     if request.method == "POST":
#         student = request.form.get("student")
#         lecturer = request.form.get("lecturer")
#         appointment_date = request.form.get("appointment_date")
#         appointment_time = request.form.get("appointment_time")
#         purpose = request.form.get("purpose")

#         # Check if all required fields are provided
#         if student and lecturer and appointment_date and appointment_time and purpose:
#             # Create the appointment
#             create_appointment(
#                 student,
#                 lecturer,
#                 appointment_date,
#                 appointment_time,
#                 purpose,
#                 status="Pending",
#             )

#             # Redirect to the appointment page with a success message
#             return render_template(
#                 "appointment.html", message="Appointment created successfully"
#             )
#         else:
#             # If any required field is missing, show an error message
#             return render_template(
#                 "appointment.html", message="Missing required field(s)"
#             )
#     else:
#         # If the request method is not POST, render the appointment page
#         return render_template("appointment.html")


# # Function to list a student's appointment(s)
# @app.route("/appointments", methods=["GET"])
# def list_appointments():
#     student = request.args.get("student")
#     if student:
#         # Retrieve appointments for the specified student
#         appointments = get_appointments(student)
#         return render_template("appointments.html", appointments=appointments)
#     else:
#         # If no student is specified, show a message
#         return render_template("appointment.html", message="No student specified")


# # Route to update an appointment
# @app.route("/update_appointment", methods=["POST"])
# def update_appointments(appointment_id):
#     if request.method == "POST":
#         # Extract new details from the form
#         new_date = request.form.get("new_date")
#         new_time = request.form.get("new_time")
#         new_purpose = request.form.get("new_purpose")

#         # Update the appointment with the new details
#         update_appointment(appointment_id, new_date, new_time, new_purpose)

#         # Redirect to the list of appointments
#         return redirect(url_for("list_appointments"))


# # Route to delete an appointment
# @app.route("/delete_appointment", methods=["POST"])
# def delete_appointment(appointment_id):
#     if request.method == "POST":
#         # Delete the specified appointment
#         delete_appointment(appointment_id)

#         # Redirect to the list of appointments
#         return redirect(url_for("list_appointments"))



@app.route("/flash")
def flash():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (session["id"],))
    user_data = cursor.fetchone()
    conn.close()

    session["username"] = user_data[1]

    return render_template("messageflashing.html",username=user_data["username"])


@app.route("/appointment")
def appointment():
    return render_template("appointment.html")



@app.route("/appointment2")
def appointment2():
    return render_template("appointment2.html")






@app.route("/appointmentcontrol")
def appointmentcontrol():
    return render_template("appointment_control.html")



@app.route("/changepassword")
def changepassword():
    return render_template("changepassword.html")



@app.route("/history")
def history():
    return render_template("history.html")


@app.route("/faculty")
def faculty():
    # Retrieve faculty information from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT faculty_name, faculty_image FROM facultyhub")
    faculty_info = cursor.fetchall()
    conn.close()

    # Render the faculty.html template with the faculty_info variable
    return render_template("faculty.html", faculty_info=faculty_info)


@app.route("/facultyhub/<int:hub_id>", methods=["GET"])
def faculty_hub_page(hub_id=None):
    try:
        if hub_id:
            # Retrieve faculty hub information from the database based on hub_id
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name, image_path FROM facultyhub WHERE id = ?", (hub_id,)
            )
            cursor.execute(
                "SELECT name, image_path FROM facultyhub WHERE id = ?", (hub_id,)
            )
            faculty_hub = cursor.fetchone()
            conn.close()

            if faculty_hub:
                # Render the faculty hub page with the relevant information
                return render_template("facultyhub.html", faculty_hub=faculty_hub)
            else:
                # If faculty hub not found, render an error page or redirect to another page
                return render_template("error.html", message="Faculty Hub Not Found")
        else:
            # Handle the case when hub_id is not provided
            return render_template(
                "error.html", message="Please provide a valid Faculty Hub ID"
            )
            return render_template(
                "error.html", message="Please provide a valid Faculty Hub ID"
            )
    except Exception as e:
        print("Error in faculty_hub_page:", e)
        return render_template(
            "error.html", message="An error occurred while processing your request"
        )
        return render_template(
            "error.html", message="An error occurred while processing your request"
        )


@app.route("/createfacultyhub", methods=["GET", "POST"])
def create_faculty_hub():
    if request.method == "POST":
        faculty_name = request.form.get("faculty_name")
        faculty_image = request.files.get("faculty_image")

        if not faculty_name or not faculty_image:
            return render_template(
                "createfacultyhub.html", message="Missing required fields"
            )

        try:
            # Save image to server
            if not os.path.exists(app.config["UPLOAD_FOLDER"]):
                os.makedirs(app.config["UPLOAD_FOLDER"])

            image_path = os.path.join(
                app.config["UPLOAD_FOLDER"], faculty_image.filename
            )
            print("Image Path:", image_path)  # Debugging print statement

            faculty_image.save(image_path)

            # Insert faculty hub info into database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO facultyhub (faculty_name, faculty_image) VALUES (?, ?)",
                (faculty_name, image_path),
            )
            conn.commit()

            conn.close()
            print("Faculty hub created successfully!")  # Debugging print statement
            return redirect(url_for("create_faculty_hub"))
        except Exception as e:
            print("Error occurred:", e)  # Debugging print statement
            return render_template(
                "createfacultyhub.html",
                message="An error occurred while creating faculty hub",
            )

    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM facultyhub")
        faculty_hubs = cursor.fetchall()
        conn.close()
        return render_template("createfacultyhub.html", faculty_hubs=faculty_hubs)


@app.route("/signoutflash")
def signoutflash():
    return render_template("signoutflash.html")



@app.route("/signoutflash2")
def signoutflash2():
    return render_template("signoutflash2.html")



@app.route("/signupflash")
def sigupflash():
    return render_template("signupflash.html")


@app.route("/profile")

@app.route("/profile")
def profile():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (session["id"],))
    user_data = cursor.fetchone()
    conn.close()

    session["username"] = user_data[3]
    session["role"] = user_data[1]
    session["faculty"] = user_data[2]
    session["email"] = user_data[4]
    session["phone_number"] = user_data[5]

    return render_template(
        "profile.html",
        username=user_data["username"],
        email=user_data["email"],
        faculty=user_data["faculty"],
        phone_number=user_data["phone_number"],
        role=user_data["role"],
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/signoutflash")





if __name__ == "__main__":
    # Run the application
    app.run(debug=True, port=6969)
