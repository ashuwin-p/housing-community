from flask import Flask, render_template, request, redirect, url_for
from client import Client
from client import (
    Client_Validation_Exception,
    InvalidNameError,
    InvalidNumberError,
    InvalidEmailError,
    InvalidPasswordError,
    Client_DB_Support,
)

app = Flask(__name__)


@app.route("/")
def login():
    return render_template("cl.html")


@app.route("/login", methods=["POST"])
def login_user():
    email = request.form["email"]
    password = request.form["password"]

    if Client_DB_Support.check_client_credential(email, password):
        return redirect(
            url_for("client_facilities")
        )  # Redirect to client_facilities.html
    else:
        return "Invalid credentials. Please try again or sign up."


@app.route("/cr.html")
def registration_form():
    return render_template("cr.html")


@app.route("/client_facilities")
def client_facilities():
    return render_template("client_facilities.html")


@app.route("/submit", methods=["POST"])
def submit_form():
    name = request.form["name"]
    phone = request.form["phone"]
    email = request.form["email"]
    password = request.form["password"]

    try:
        Client.create_client(name, phone, email, password)
        return "Registration Successful"
    except InvalidNameError:
        return "Invalid Name: Please enter a valid name."
    except InvalidNumberError:
        return "Invalid Phone Number: Please enter a valid phone number."
    except InvalidEmailError:
        return "Invalid Email: Please enter a valid Email address."
    except InvalidPasswordError:
        return "Invalid Password: Password must be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, and one digit."
    except Exception as e:
        return "Error: Registration failed. Please check your details and try again."


if __name__ == "__main__":
    app.run(debug=True)
