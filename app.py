from flask import Flask, render_template,session, redirect, url_for, request, flash
from config import Config
from database import db
import models  # IMPORTANT: ensures models are registered


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()  # creates tables if not exist

    @app.route("/")
    def index():
        if "user_id" not in session:
            flash("Please log in to view your tasks.")
            return redirect(url_for("login"))
        
        return render_template("index.html")
    
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            user = models.User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session["user_id"] = user.id
                flash("Logged in successfully!")
                return redirect(url_for("index"))
            else:
                flash("Invalid username or password.")
        
        return render_template("login.html")
    
    


    return app



app = create_app()

if __name__ == "__main__":
    app.run(debug=True)