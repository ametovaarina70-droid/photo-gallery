import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash

from app import app, init_db, DATABASE


DEMO_PASSWORD = "password123"

DEMO_USERS = [
    "julia",
    "bogdan",
    "mina",
    "jun",
]

DEMO_PHOTOS = [
    {
        "username": "julia",
        "filename": "demo_seoul_street.png",
        "description": "A sunny street photo from a walk in Seoul.",
        "keywords": "seoul street city walk sunny",
    },
    {
        "username": "julia",
        "filename": "demo_coffee_table.png",
        "description": "Coffee and cake at a cozy cafe.",
        "keywords": "coffee cake cafe",
    },
    {
        "username": "bogdan",
        "filename": "demo_university_campus.png",
        "description": "University campus view in the afternoon.",
        "keywords": "university campus student afternoon",
    },
    {
        "username": "bogdan",
        "filename": "demo_night_city.png",
        "description": "Night city lights after class.",
        "keywords": "night city lights evening",
    },
    {
        "username": "mina",
        "filename": "demo_flowers.png",
        "description": "Flowers in the park during spring.",
        "keywords": "flowers park spring nature",
    },
    {
        "username": "jun",
        "filename": "demo_beach.png",
        "description": "Simple beach photo from a weekend trip.",
        "keywords": "beach weekend sea travel",
    },
]

DEMO_MESSAGES = [
    ("bogdan", "julia", 1, "Hi Julia, I like this city photo. Where did you take it?"),
    ("mina", "julia", 2, "This cafe photo looks nice. Can you recommend this place?"),
    ("julia", "bogdan", 3, "Your campus photo is clear and beautiful."),
    ("jun", "mina", 5, "Nice flowers. This looks like spring season."),
]


def get_user_id(db, username):
    row = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    return row[0] if row else None


def get_photo_id_by_position(db, position):
    photos = db.execute("SELECT id FROM photos ORDER BY id").fetchall()
    if 1 <= position <= len(photos):
        return photos[position - 1][0]
    return None


def main():
    with app.app_context():
        init_db()

    db = sqlite3.connect(DATABASE)
    try:
        now = datetime.now().isoformat(timespec="seconds")

        for username in DEMO_USERS:
            existing = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
            if existing is None:
                db.execute(
                    "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
                    (username, generate_password_hash(DEMO_PASSWORD), now),
                )

        db.commit()

        for item in DEMO_PHOTOS:
            user_id = get_user_id(db, item["username"])
            existing = db.execute(
                "SELECT id FROM photos WHERE user_id = ? AND filename = ?",
                (user_id, item["filename"]),
            ).fetchone()
            if existing is None:
                db.execute(
                    """
                    INSERT INTO photos (user_id, filename, description, keywords, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        user_id,
                        item["filename"],
                        item["description"],
                        item["keywords"],
                        now,
                    ),
                )

        db.commit()

        for sender, receiver, photo_position, body in DEMO_MESSAGES:
            sender_id = get_user_id(db, sender)
            receiver_id = get_user_id(db, receiver)
            photo_id = get_photo_id_by_position(db, photo_position)
            existing = db.execute(
                """
                SELECT id FROM messages
                WHERE sender_id = ? AND receiver_id = ? AND body = ?
                """,
                (sender_id, receiver_id, body),
            ).fetchone()
            if existing is None:
                db.execute(
                    """
                    INSERT INTO messages (sender_id, receiver_id, photo_id, body, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (sender_id, receiver_id, photo_id, body, now),
                )

        db.commit()

        user_count = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        photo_count = db.execute("SELECT COUNT(*) FROM photos").fetchone()[0]
        message_count = db.execute("SELECT COUNT(*) FROM messages").fetchone()[0]

        print("Demo data added successfully.")
        print(f"Users: {user_count}")
        print(f"Photos: {photo_count}")
        print(f"Messages: {message_count}")
        print("")
        print("Demo login accounts:")
        for username in DEMO_USERS:
            print(f"  username: {username} | password: {DEMO_PASSWORD}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
