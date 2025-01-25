from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import User
from os import getenv
from flask import session

# Set up SQLAlchemy engine and session
DATABASE_URL = getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def get_logged_in_user():
    """
    Retrieve the logged-in user from the session and database.
    """
    user_info = session.get('user_info')  # Fetch user info from the session
    print("user_info:", user_info)

    if not user_info or 'email' not in user_info:
        return None

    session_db = Session()
    try:
        user = session_db.query(User).filter_by(email=user_info['email']).first()
        return user
    finally:
        session_db.close()
