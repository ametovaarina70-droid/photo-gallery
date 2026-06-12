import os
import sqlite3
from functools import wraps
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    g,
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "gallery.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-secret-key-for-your-local-project"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


# ----------------------------
# Database helper functions
# ----------------------------
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            description TEXT NOT NULL,
            keywords TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            photo_id INTEGER,
            body TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (sender_id) REFERENCES users (id),
            FOREIGN KEY (receiver_id) REFERENCES users (id),
            FOREIGN KEY (photo_id) REFERENCES photos (id)
        )
        """
    )
    db.commit()


@app.cli.command("init-db")
def init_db_command():
    init_db()
    print("Database initialized.")


@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT id, username FROM users WHERE id = ?", (user_id,)
        ).fetchone()


@app.context_processor
def inject_current_user():
    return {"current_user": g.get("user")}


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash("Please sign in first.", "warning")
            return redirect(url_for("login"))
        return view(**kwargs)

    return wrapped_view


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def unique_filename(original_filename):
    safe_name = secure_filename(original_filename)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    return f"{timestamp}_{safe_name}"


# ----------------------------
# Routes: user authentication
# ----------------------------
@app.route("/")
def index():
    return redirect(url_for("users"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and password are required.", "danger")
            return render_template("signup.html")

        db = get_db()
        existing_user = db.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        ).fetchone()
        if existing_user:
            flash("This username is already used.", "danger")
            return render_template("signup.html")

        db.execute(
            "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
            (username, generate_password_hash(password), datetime.now().isoformat(timespec="seconds")),
        )
        db.commit()
        flash("Account created. Please sign in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = get_db().execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()

        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid username or password.", "danger")
            return render_template("login.html")

        session.clear()
        session["user_id"] = user["id"]
        flash("Signed in successfully.", "success")
        return redirect(url_for("gallery"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Signed out successfully.", "info")
    return redirect(url_for("users"))


# ----------------------------
# Routes: users and photos
# ----------------------------
@app.route("/users")
def users():
    all_users = get_db().execute(
        "SELECT id, username, created_at FROM users ORDER BY username"
    ).fetchall()
    return render_template("users.html", users=all_users)


@app.route("/gallery")
@login_required
def gallery():
    photos = get_db().execute(
        """
        SELECT photos.*, users.username
        FROM photos
        JOIN users ON photos.user_id = users.id
        ORDER BY photos.created_at DESC
        """
    ).fetchall()
    return render_template("gallery.html", photos=photos)


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        description = request.form.get("description", "").strip()
        keywords = request.form.get("keywords", "").strip()
        photo = request.files.get("photo")

        if not description or not keywords:
            flash("Description and keywords are required.", "danger")
            return render_template("upload.html")

        if photo is None or photo.filename == "":
            flash("Please choose a photo file.", "danger")
            return render_template("upload.html")

        if not allowed_file(photo.filename):
            flash("Only png, jpg, jpeg, and gif files are allowed.", "danger")
            return render_template("upload.html")

        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        filename = unique_filename(photo.filename)
        photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        get_db().execute(
            """
            INSERT INTO photos (user_id, filename, description, keywords, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                g.user["id"],
                filename,
                description,
                keywords,
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        get_db().commit()
        flash("Photo uploaded successfully.", "success")
        return redirect(url_for("gallery"))

    return render_template("upload.html")


@app.route("/photo/<int:photo_id>/edit", methods=["GET", "POST"])
@login_required
def edit_photo(photo_id):
    photo = get_db().execute(
        "SELECT * FROM photos WHERE id = ?", (photo_id,)
    ).fetchone()

    if photo is None:
        flash("Photo not found.", "danger")
        return redirect(url_for("gallery"))

    if photo["user_id"] != g.user["id"]:
        flash("You can edit only your own photo information.", "danger")
        return redirect(url_for("gallery"))

    if request.method == "POST":
        description = request.form.get("description", "").strip()
        keywords = request.form.get("keywords", "").strip()

        if not description or not keywords:
            flash("Description and keywords are required.", "danger")
            return render_template("edit_photo.html", photo=photo)

        get_db().execute(
            "UPDATE photos SET description = ?, keywords = ? WHERE id = ?",
            (description, keywords, photo_id),
        )
        get_db().commit()
        flash("Photo information updated.", "success")
        return redirect(url_for("gallery"))

    return render_template("edit_photo.html", photo=photo)


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    photos = []
    keyword = ""
    searched = False

    if request.method == "POST":
        searched = True
        keyword = request.form.get("keyword", "").strip()
        if keyword:
            photos = get_db().execute(
                """
                SELECT photos.*, users.username
                FROM photos
                JOIN users ON photos.user_id = users.id
                WHERE LOWER(photos.keywords) LIKE LOWER(?)
                ORDER BY photos.created_at DESC
                """,
                (f"%{keyword}%",),
            ).fetchall()
        else:
            flash("Please enter a keyword.", "warning")

    return render_template("search.html", photos=photos, keyword=keyword, searched=searched)


# ----------------------------
# Routes: direct messages
# ----------------------------
@app.route("/message/photo/<int:photo_id>", methods=["GET", "POST"])
@login_required
def send_message(photo_id):
    photo = get_db().execute(
        """
        SELECT photos.*, users.username
        FROM photos
        JOIN users ON photos.user_id = users.id
        WHERE photos.id = ?
        """,
        (photo_id,),
    ).fetchone()

    if photo is None:
        flash("Photo not found.", "danger")
        return redirect(url_for("gallery"))

    if request.method == "POST":
        body = request.form.get("body", "").strip()
        if not body:
            flash("Message text is required.", "danger")
            return render_template("send_message.html", photo=photo)

        get_db().execute(
            """
            INSERT INTO messages (sender_id, receiver_id, photo_id, body, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                g.user["id"],
                photo["user_id"],
                photo_id,
                body,
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        get_db().commit()
        flash("Direct message sent.", "success")
        return redirect(url_for("gallery"))

    return render_template("send_message.html", photo=photo)


@app.route("/inbox")
@login_required
def inbox():
    messages = get_db().execute(
        """
        SELECT messages.*, sender.username AS sender_name, photos.filename, photos.description AS photo_description
        FROM messages
        JOIN users AS sender ON messages.sender_id = sender.id
        LEFT JOIN photos ON messages.photo_id = photos.id
        WHERE messages.receiver_id = ?
        ORDER BY messages.created_at DESC
        """,
        (g.user["id"],),
    ).fetchall()
    return render_template("inbox.html", messages=messages)


@app.route("/message/<int:message_id>/reply", methods=["GET", "POST"])
@login_required
def reply_message(message_id):
    original = get_db().execute(
        """
        SELECT messages.*, sender.username AS sender_name
        FROM messages
        JOIN users AS sender ON messages.sender_id = sender.id
        WHERE messages.id = ? AND messages.receiver_id = ?
        """,
        (message_id, g.user["id"]),
    ).fetchone()

    if original is None:
        flash("Message not found.", "danger")
        return redirect(url_for("inbox"))

    if request.method == "POST":
        body = request.form.get("body", "").strip()
        if not body:
            flash("Reply text is required.", "danger")
            return render_template("reply_message.html", original=original)

        get_db().execute(
            """
            INSERT INTO messages (sender_id, receiver_id, photo_id, body, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                g.user["id"],
                original["sender_id"],
                original["photo_id"],
                body,
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        get_db().commit()
        flash("Reply sent.", "success")
        return redirect(url_for("inbox"))

    return render_template("reply_message.html", original=original)


@app.route("/message/<int:message_id>/delete", methods=["POST"])
@login_required
def delete_message(message_id):
    message = get_db().execute(
        "SELECT * FROM messages WHERE id = ? AND receiver_id = ?",
        (message_id, g.user["id"]),
    ).fetchone()

    if message is None:
        flash("Message not found.", "danger")
        return redirect(url_for("inbox"))

    get_db().execute("DELETE FROM messages WHERE id = ?", (message_id,))
    get_db().commit()
    flash("Message deleted.", "info")
    return redirect(url_for("inbox"))


if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    with app.app_context():
        init_db()
    app.run(debug=True)
