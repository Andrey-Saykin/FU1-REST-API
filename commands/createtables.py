import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import Base, engine

def create_tables():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    create_tables()