# User Manual: Personal Photo Gallery

## Project Name

Personal Photo Gallery

## Purpose

This website allows registered users to upload personal photos and send direct messages to other users through photo posts.

## How to Run the Software

### Step 1: Install Python

Install Python 3.10 or newer.

### Step 2: Open the Project Folder

Open terminal or command prompt inside the project folder.

### Step 3: Install Required Packages

Run:

```bash
pip install -r requirements.txt
```

### Step 4: Create the Database

Run:

```bash
flask --app app init-db
```

### Step 5: Start the Website

Run:

```bash
python app.py
```

### Step 6: Open Browser

Go to:

```text
http://127.0.0.1:5000
```

## Provided Functionalities

### 1. Sign Up

A new user can create an account with username and password.

### 2. Sign In

An existing user can sign in with username and password.

### 3. Sign Out

A signed user can sign out using the Sign Out button.

### 4. User List

Every visitor can see the user list. This includes guests who are not signed in.

### 5. Photo Gallery

Only signed users can see uploaded photos.

### 6. Upload Photo

A signed user can upload a photo with:

- photo file
- textual description
- keywords

### 7. Edit Photo Information

A user can edit only his or her own photo description and keywords.

### 8. Keyword Search

A signed user can search photos by keyword. The result page shows photos where the keyword matches the saved photo keywords.

### 9. Direct Message

Every photo post has a Direct Message button. A signed user can send a message to the uploader of the photo.

### 10. Inbox

When a user signs in, the user can open Inbox and see messages sent to him or her.

### 11. Reply Message

Each received message has a Reply button.

### 12. Delete Message

Each received message has a Delete button.

## Important Notes

Guests can only see the user list. Guests cannot see photos and cannot upload photos.

The project is intended to run locally on one PC.
