"""
Seed script to populate the database with initial data.
"""
from app import app, db


def seed_database():
    """Seed the database with initial data."""
    with app.app_context():
        # Add seed data here
        pass


if __name__ == "__main__":
    seed_database()
    print("Database seeded successfully!")
