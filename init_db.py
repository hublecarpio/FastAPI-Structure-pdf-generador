import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import engine, Base
from app.models.user import User
from app.models.template import Template
from app.models.apikey import APIKey
from app.models.renderlog import RenderLog
from app.core.security import get_password_hash
from sqlalchemy.orm import Session


def init_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def create_admin_user(email: str = "admin@example.com", password: str = "admin123"):
    from app.core.database import SessionLocal
    
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"Admin user '{email}' already exists.")
            return existing_user
        
        hashed_password = get_password_hash(password)
        admin = User(email=email, hashed_password=hashed_password)
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print(f"Admin user '{email}' created successfully!")
        return admin
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
    
    if "--admin" in sys.argv:
        admin_email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
        admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")
        create_admin_user(admin_email, admin_password)
