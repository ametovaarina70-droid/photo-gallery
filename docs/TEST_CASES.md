# Test Cases

## TC01: Sign Up

**Precondition:** User is not registered.

**Steps:**
1. Open `/signup`.
2. Enter username and password.
3. Submit the form.

**Expected result:** Account is created and user is redirected to sign in page.

## TC02: Sign In

**Precondition:** User account exists.

**Steps:**
1. Open `/login`.
2. Enter correct username and password.
3. Submit the form.

**Expected result:** User is signed in and redirected to gallery.

## TC03: Sign Out

**Precondition:** User is signed in.

**Steps:**
1. Click Sign Out.

**Expected result:** Session is cleared and user returns to public user list.

## TC04: Guest Can See User List

**Precondition:** User is not signed in.

**Steps:**
1. Open `/users`.

**Expected result:** User list is visible.

## TC05: Guest Cannot See Gallery

**Precondition:** User is not signed in.

**Steps:**
1. Open `/gallery`.

**Expected result:** User is redirected to sign in page.

## TC06: Upload Photo

**Precondition:** User is signed in.

**Steps:**
1. Open `/upload`.
2. Select image file.
3. Enter description.
4. Enter keywords.
5. Submit the form.

**Expected result:** Photo is saved and visible in gallery.

## TC07: Edit Own Photo Information

**Precondition:** User is signed in and has uploaded a photo.

**Steps:**
1. Open gallery.
2. Click Edit Photo Information on own photo.
3. Change description or keywords.
4. Save.

**Expected result:** Updated description and keywords are visible in gallery.

## TC08: Search Photos by Keyword

**Precondition:** User is signed in and photos exist.

**Steps:**
1. Open `/search`.
2. Enter keyword used in a photo.
3. Submit.

**Expected result:** Photos matching this keyword are shown.

## TC09: Send Direct Message

**Precondition:** User is signed in and photo exists.

**Steps:**
1. Open gallery.
2. Click Direct Message on a photo.
3. Enter message text.
4. Submit.

**Expected result:** Message is saved and sent to photo uploader.

## TC10: See Inbox

**Precondition:** User is signed in and has received messages.

**Steps:**
1. Open `/inbox`.

**Expected result:** Received messages are listed.

## TC11: Reply to Message

**Precondition:** User is signed in and has a received message.

**Steps:**
1. Open inbox.
2. Click Reply.
3. Enter reply text.
4. Submit.

**Expected result:** Reply is sent to original sender.

## TC12: Delete Message

**Precondition:** User is signed in and has a received message.

**Steps:**
1. Open inbox.
2. Click Delete.

**Expected result:** Message is deleted from inbox.
