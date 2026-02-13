from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from config import Config
from database import db
import models
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models import User, Event


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # ------------------------
    # Login Manager Setup
    # ------------------------
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.unauthorized_handler
    def unauthorized():
        if request.path.startswith("/api/"):
            return jsonify({"error": "Unauthorized"}), 401
        return redirect(url_for("login"))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ------------------------
    # Create tables
    # ------------------------
    with app.app_context():
        db.create_all()

    # ------------------------
    # Routes
    # ------------------------

    @app.route("/")
    @login_required
    def index():
        return render_template("index.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                login_user(user)   # ✅ Correct way
                flash("Logged in successfully!")
                return redirect(url_for("index"))
            else:
                flash("Invalid username or password.")

        return render_template("login.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        flash("Logged out.")
        return redirect(url_for("login"))


    @app.route("/api/events", methods=["POST"])
    
    def get_events():

        data = request.json
        group_ids = data.get("group_ids", [])

        # convert to int
        group_ids = [int(gid) for gid in group_ids]

        # groups user belongs to
        allowed_groups = [link.group_id for link in current_user.group_links]

        valid_groups = [gid for gid in group_ids if gid in allowed_groups]

        if not valid_groups:
            return jsonify([])

        events = Event.query.filter(Event.group_id.in_(valid_groups)).all()

        return jsonify([
            {
                "id": e.id,
                "title": e.title,
                "start": e.start_time.isoformat(),
                "end": e.end_time.isoformat()
            }
            for e in events
    ])

    return app

    



app = create_app()

if __name__ == "__main__":
    app.run(debug=True)