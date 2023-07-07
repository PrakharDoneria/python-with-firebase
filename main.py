import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase SDK
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Function to create a new user account
def create_account(email, password, username):
    try:
        # Create user in Firebase Authentication
        user = firebase_admin.auth.create_user(email=email, password=password)
        
        # Store user details in Firestore database
        user_ref = db.collection('users').document(user.uid)
        user_ref.set({
            'email': email,
            'username': username
        })
        
        print("Account created successfully!")
        return user
    except Exception as e:
        print("Failed to create account:", str(e))
        return None

# Function to authenticate a user
def authenticate(email, password):
    try:
        user = firebase_admin.auth.get_user_by_email(email)
        firebase_admin.auth.get_user(user.uid)  # Refresh user data
        user = firebase_admin.auth.authenticate(email=email, password=password)
        if user:
            print("Authentication successful!")
            return user
        else:
            print("Invalid email or password.")
            return None
    except Exception as e:
        print("Authentication failed:", str(e))
        return None

# Function to create a new post
def create_post(user, content):
    try:
        # Store the post in Firestore database
        post_ref = db.collection('posts').document()
        post_ref.set({
            'author_id': user.uid,
            'content': content,
            'likes': 0,
            'comments': []
        })
        
        print("Post created successfully!")
        return post_ref.id
    except Exception as e:
        print("Failed to create post:", str(e))
        return None

# Function to like a post
def like_post(user, post_id):
    try:
        # Update the likes count in the post document
        post_ref = db.collection('posts').document(post_id)
        post_ref.update({
            'likes': firestore.Increment(1)
        })
        
        print("Post liked successfully!")
    except Exception as e:
        print("Failed to like post:", str(e))

# Function to add a comment to a post
def add_comment(user, post_id, comment):
    try:
        # Add the comment to the comments array in the post document
        post_ref = db.collection('posts').document(post_id)
        post_ref.update({
            'comments': firestore.ArrayUnion([comment])
        })
        
        print("Comment added successfully!")
    except Exception as e:
        print("Failed to add comment:", str(e))

# Example usage:
email = "example@example.com"
password = "password"
username = "example_user"

# Create a new user account
user = create_account(email, password, username)

if user:
    # Create a new post
    post_content = "This is a sample post."
    post_id = create_post(user, post_content)
    
    # Like the post
    like_post(user, post_id)
    
    # Add a comment to the post
    comment = "Great post!"
    add_comment(user, post_id, comment)
