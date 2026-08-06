#!/usr/bin/env python3
"""
Initialize the database. Run once before first collection.
"""

from src.database import init_db

if __name__ == '__main__':
    init_db()
    print("Run: python scripts/setup_db.py")