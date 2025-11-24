import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Read the connection string from the environment
DATABASE_URL = os.environ.get("DATABASE_URL")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True, future=True)

# Create a session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
