from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    print("--- Create Admin User ---")
    username = input("Enter Admin Username: ")
    email = input("Enter Admin Email: ")
    password = input("Enter Admin Password: ")
    
    if User.query.filter_by(email=email).first():
        print(f"Error: User with email '{email}' already exists!")
    elif User.query.filter_by(username=username).first():
        print(f"Error: User with username '{username}' already exists!")
    else:
        user = User(username=username, email=email, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"Success! Admin user '{username}' created.")
