# Personal Photo Gallery

This is a simple web-based personal photo gallery project made with Python Flask, HTML, CSS, JavaScript, Bootstrap, and SQLite.

The website follows only the required functions from the assignment:

- Sign up, sign in, and sign out
- Public user list
- Signed users can see all photos
- Guests can see only the user list
- Signed users can upload photos with description and keywords
- Photo owner can edit photo description and keywords
- Signed users can search photos by keyword
- Signed users can send direct messages from photo posts
- Signed users can see inbox messages
- Signed users can reply to messages
- Signed users can delete received messages

No extra functions were added.

## 1. Requirements

Install Python 3.10 or newer.

Install project packages:

```bash
pip install -r requirements.txt
```

## 2. How to Run

Open the project folder in terminal.

Initialize the database:

```bash
flask --app app init-db
```

Run the server:

```bash
python app.py
```

Open the browser and go to:

```text
http://127.0.0.1:5000
```

## 3. Main Pages

| Page | URL | Access |
|---|---|---|
| User list | `/users` | Everyone |
| Sign up | `/signup` | Everyone |
| Sign in | `/login` | Everyone |
| Gallery | `/gallery` | Signed users only |
| Upload | `/upload` | Signed users only |
| Search | `/search` | Signed users only |
| Inbox | `/inbox` | Signed users only |

## 4. Database Tables

The project uses three SQLite tables:

- `users`
- `photos`
- `messages`



## 5. Deploy to Vercel

On your computer the app uses SQLite (`gallery.db`) and saves photos in `public/static/uploads/`.
Vercel's disk is temporary, so online the app uses:

- **Postgres** for users, photos and messages (set `DATABASE_URL` or `POSTGRES_URL`)
- **Vercel Blob** for uploaded photos (set `BLOB_READ_WRITE_TOKEN`)
- **`SECRET_KEY`** to protect sign-in sessions (any long random text)

Steps:

1. Import this GitHub repository as a new project on vercel.com.
2. In the project, open **Storage** and add a **Postgres** database (Neon) and a **Blob** store (public access). Vercel adds their environment variables for you.
3. In **Settings → Environment Variables**, add `SECRET_KEY`.
4. Redeploy. The tables are created automatically on the first visit.
