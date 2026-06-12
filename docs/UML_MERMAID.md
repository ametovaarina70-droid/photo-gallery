# UML Diagrams in Mermaid Format

You can paste these diagrams into a Mermaid editor or GitHub Markdown.

## Use Case Diagram

```mermaid
usecaseDiagram
actor Guest
actor SignedUser
Guest --> (See user list)
Guest --> (Sign up)
Guest --> (Sign in)
SignedUser --> (Sign out)
SignedUser --> (See user list)
SignedUser --> (See all photos)
SignedUser --> (Upload photo)
SignedUser --> (Edit own photo information)
SignedUser --> (Search photos by keyword)
SignedUser --> (Send direct message)
SignedUser --> (See inbox)
SignedUser --> (Reply to message)
SignedUser --> (Delete received message)
```

## Class Diagram

```mermaid
classDiagram
class User {
  int id
  string username
  string password_hash
  string created_at
}

class Photo {
  int id
  int user_id
  string filename
  string description
  string keywords
  string created_at
}

class Message {
  int id
  int sender_id
  int receiver_id
  int photo_id
  string body
  string created_at
}

User "1" --> "many" Photo
User "1" --> "many" Message : sends
User "1" --> "many" Message : receives
Photo "1" --> "many" Message
```

## Simple Sequence: Upload Photo

```mermaid
sequenceDiagram
participant User
participant Browser
participant FlaskApp
participant SQLite
User->>Browser: Fill upload form
Browser->>FlaskApp: POST /upload
FlaskApp->>FlaskApp: Validate sign in and file type
FlaskApp->>SQLite: Save photo information
FlaskApp->>Browser: Redirect to gallery
Browser->>User: Show uploaded photo
```

## Simple Sequence: Direct Message

```mermaid
sequenceDiagram
participant Sender
participant Browser
participant FlaskApp
participant SQLite
participant Receiver
Sender->>Browser: Click Direct Message
Browser->>FlaskApp: GET /message/photo/{id}
Sender->>Browser: Write message
Browser->>FlaskApp: POST message
FlaskApp->>SQLite: Save message
Receiver->>Browser: Open inbox
Browser->>FlaskApp: GET /inbox
FlaskApp->>SQLite: Load received messages
Browser->>Receiver: Show message with reply/delete buttons
```
