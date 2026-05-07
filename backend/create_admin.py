#!/usr/bin/env python3
"""Script to create admin user for development."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine
from app.models import Base, User
from app.services.auth_service import hash_password

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Check if modern admin user already exists
    existing = db.query(User).filter(User.email == "admin@example.com").first()
    if existing:
        print("Admin user already exists. Updating password...")
        existing.hashed_password = hash_password("4173")
        db.commit()
        print("[OK] Admin password updated")
    else:
        # Upgrade legacy admin user if present
        legacy_admin = db.query(User).filter(User.email == "admin").first()
        if legacy_admin:
            legacy_admin.email = "admin@example.com"
            legacy_admin.hashed_password = hash_password("4173")
            db.commit()
            print("[OK] Legacy admin upgraded to admin@example.com")
        else:
            # Create new admin user
            admin = User(
                email="admin@example.com",
                hashed_password=hash_password("4173"),
                full_name="Admin User",
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("[OK] Admin user created successfully")
            print("  Email: admin@example.com")
            print("  Password: 4173")
finally:
    db.close()
