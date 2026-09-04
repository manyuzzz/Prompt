"""Run this script to seed the database with initial data."""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seed_data import seed_all

if __name__ == "__main__":
    asyncio.run(seed_all())
