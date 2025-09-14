from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import User
from extensions import db, login_manager
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import random

auth_bp = Blueprint("auth", __name__)

WORDS = ["cop", "hide", "spy", "agent", "fbi", "clue", "case", "shadow", "hunter"]

def generate_username():
    return f"detective-{random.choice(WORDS)}-{random.randint(100, 999)}"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "error")
            return redirect(url_for("auth.signup"))

        # Generate unique username
        username = generate_username()
        while User.query.filter_by(username=username).first():
            username = generate_username()

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = User(
            email=email,
            password=hashed_password,
            username=username
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        session['username'] = username  
        flash("Account created successfully!", "success")
        return redirect(url_for("auth.signup"))  

    return render_template("signup.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Invalid email or password.", "error")
            return redirect(url_for("auth.login"))

        login_user(user)
        return redirect(url_for("home"))

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("auth.login"))