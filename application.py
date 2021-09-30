import os

#from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///yourtutors.db")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    print("hello")